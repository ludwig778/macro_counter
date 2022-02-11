from copy import deepcopy
from enum import Enum, auto

from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from pyparsing import ParseFatalException
from tabulate import tabulate

from macro_counter.adapters import get_adapters
from macro_counter.app.parsers import app_parser
from macro_counter.exceptions import ComponentDoesNotExist
from macro_counter.fields import attrs_fields, macro_fields, unit_field
from macro_counter.models import Component, ComponentKind
from macro_counter.repositories.components import component_repository_factory
from macro_counter.utils import is_float


class PromptSignal(Enum):
    LEAVE = auto()
    QUIT = auto()


class PromptState(Enum):
    RUNNING = auto()
    STOPPED = auto()


EmptyWordCompleter = WordCompleter([])


def get_measure(component: Component):
    if component.kind == ComponentKind.SOLID:
        return "gr"
    else:
        return "ml"


class AppPrompt:
    def __init__(self):
        self.adapters = get_adapters()
        self.repo = component_repository_factory(self.adapters.current)(
            self.adapters.current
        )
        self.state = PromptState.STOPPED
        self.history = FileHistory(".macro_counter_history")

        if self.adapters.current is self.adapters.mongo:
            self.print("Using mongo store")
        else:
            if self.adapters.mongo is not None:
                self.print("Unable to connect to the configured mongo cluster")

            self.print("Using local file store")

        self.completer = None
        self.reset_completer()

    def prompt(self, message, completer=None, use_history=True):
        return prompt(
            message=message,
            history=self.history if use_history else None,
            completer=self.completer if completer is None else completer,
            enable_suspend=True,
        )

    def reset_completer(self):
        self.components = {component.name: component for component in self.repo.list()}
        self.completer = WordCompleter(
            [
                "+",
                "%",
                "*",
                "/",
                "=",
                "register",
                "delete",
                "detail",
                "quit",
                *sorted(self.components.keys()),
            ]
        )

    def print(self, *args, **kwargs):
        print_formatted_text(*args, **kwargs)

    def _get_kind(self, default=None):
        kind_raw = self.prompt(
            f"Type (L)iquid/(S)olid{' (' + str(default.capitalize()) + ') ' if default else ''}: ",
            completer=WordCompleter(["Solid", "Liquid"], ignore_case=True),
            use_history=False,
        )

        if not kind_raw and default:
            kind = default
        elif kind_raw.lower() in ("l", "liquid"):
            kind = "liquid"
        elif kind_raw.lower() in ("s", "solid"):
            kind = "solid"
        else:
            raise ValueError("Error: Wrong kind")

        return kind

    def _get_units(self, default=None):
        units_raw = self.prompt(
            f"Type units{' (' + str(default) + ') ' if default else ''}: ",
            use_history=False,
            completer=EmptyWordCompleter,
        )

        if not units_raw:
            units = default
        elif is_float(units_raw):
            units = float(units_raw)
        else:
            raise ValueError("Error: Wrong value, number required")

        return units

    def _get_attrs(self, defaults=None):
        attrs = deepcopy(defaults) or {}

        for field in attrs_fields:
            value = None

            if default := attrs.get(field.label):
                value = self.prompt(
                    f"How much {field.fullname} ({default}/Reset): ",
                    completer=WordCompleter(["Reset"], ignore_case=True),
                    use_history=False,
                )
            else:
                value = self.prompt(
                    f"How much {field.fullname} : ",
                    completer=EmptyWordCompleter,
                    use_history=False,
                )

            if value.lower() in ("r", "reset"):
                attrs.pop(field.label)
                value = None
            elif value:
                if is_float(value):
                    value = float(eval(value))
                else:
                    raise ValueError("Error: Wrong value, number required")
            elif default:
                value = float(default)

            if value:
                attrs[field.label] = value

        return attrs

    def create(self, name):
        self.print(f"Registering {name}")

        try:
            kind = self._get_kind()
            units = self._get_units(default=100.0)
            attrs = self._get_attrs()

        except Exception as exc:
            self.print(str(exc))

            return

        self.repo.create(Component(name=name, kind=kind, units=units, attrs=attrs))

        self.print(f"Created: {name}")
        self.reset_completer()

    def update(self, component):
        self.print(f"Updating {component.name}")

        altered = False

        try:
            kind = self._get_kind(default=component.kind)

            if kind != component.kind:
                component.kind = kind
                altered = True

            units = self._get_units(default=component.units)

            if units != component.units:
                component.units = units
                altered = True

            attrs = self._get_attrs(defaults=component.attrs)

            if attrs != component.attrs:
                component.attrs = attrs
                altered = True

        except Exception as exc:
            self.print(str(exc))

            return

        if altered:
            self.repo.update(component)

            self.print(f"Updated: {component.name}")
        else:
            self.print("Nothing changed")

    def register(self, name):
        try:
            component = self.repo.get(name)

            self.update(component)
        except ComponentDoesNotExist:
            self.create(name)

        self.reset_completer()

    def delete(self, name):
        try:
            component = self.repo.get(name)

            self.repo.delete(component)

            del self.components[name]

            self.reset_completer()
            self.print(f"Component {name} deleted")

        except ComponentDoesNotExist:
            self.print(f"Component {name} not found")

    def loop(self):
        self.state = PromptState.RUNNING

        while True:
            try:
                signal = self.loop_step()
                if signal == PromptSignal.LEAVE:
                    break
                if signal == PromptSignal.QUIT:
                    self.state = PromptState.STOPPED

                    return PromptSignal.QUIT
            except EOFError:
                self.print("EOF : quitting...")

                self.state = PromptState.STOPPED

                return PromptSignal.QUIT
            except KeyboardInterrupt:
                pass

        self.state = PromptState.STOPPED

    def loop_step(self):
        text = self.prompt(">>> ")

        if text in ("q", "quit"):
            self.print("quitting...")

            return PromptSignal.QUIT

        elif text in ("l", "leave"):
            self.print("leaving...")

            return PromptSignal.LEAVE

        elif text:
            try:
                if signal := self.dispatch(text):
                    return signal

            except ParseFatalException as exc:
                offset = len(self.session.message) + exc.loc

                self.print(f"{' ' * offset}^ {exc.msg}")

    def compute_components(self, parsed_components):
        components = []

        for parsed_component in parsed_components:
            component_data = parsed_component.asDict()

            if not component_data:
                continue

            component_name = component_data["name"]

            if not (component := self.components.get(component_name)):
                try:
                    component = self.repo.get(component_name)
                except ComponentDoesNotExist:
                    pass

            if not component:
                self.print(f"No component {component_name} has been found: skipping")

                continue

            if normalization := component_data.get("normalization"):
                component = component % normalization

            if operations := component_data.get("operations"):
                multiplier = 1

                for operation in operations:
                    if operation["op"] == "multiply":
                        multiplier *= operation["number"]

                    elif operation["op"] == "divide":
                        multiplier /= operation["number"]

                component = component * multiplier

            components.append(component)

        return components

    def display(self, component):
        macro_total = sum(
            [
                component.attrs[field.label]
                for field in macro_fields
                if field.label in component.attrs
            ]
        )

        rows = []

        for field in attrs_fields:
            value = component.attrs.get(field.label)

            if not value:
                continue

            field_label_cell = field.fullname
            if field.show_percents and not field.macro:
                field_label_cell = "- " + field_label_cell

            value_cell = f"{value:.1f}"

            percent_cell = None
            if field.show_percents:
                percent_cell = f"{value / macro_total * 100:.1f}%"

            rows.append([field_label_cell, value_cell, percent_cell])

        rows.insert(
            1,
            [
                unit_field.fullname,
                f"{component.units} {get_measure(component)}",
            ],
        )

        self.print(tabulate(rows))

    def display_details(self, component, components):
        rows = []

        present_fields = [
            field for field in attrs_fields if field.label in component.attrs
        ]
        present_fields.insert(0, unit_field)

        headers = ["Name"] + [field.name for field in present_fields]

        total = {field.label: 0.0 for field in present_fields}

        for component in components:
            total[unit_field.label] += component.units
            for k, v in component.attrs.items():
                total[k] = total[k] + v

        def to_percent(num, total, vv=1):
            return f"{num / (total if total else 1) * 100:.{vv}f}%"

        for component in components:
            raw_data = [component.name]
            perc_data = [None]

            for field in present_fields:
                if field is unit_field:
                    raw_data.append(str(component.units) + get_measure(component))
                    perc_data.append(
                        to_percent(component.units, total[unit_field.label])
                    )
                elif value := component.attrs.get(field.label):
                    raw_data.append(value)
                    perc_data.append(to_percent(value, total[field.label]))
                else:
                    raw_data.append(None)
                    perc_data.append(None)

            rows.append(raw_data)
            rows.append(perc_data)

        rows.append([])

        row = ["Total"]
        for field in present_fields:
            if field is unit_field:
                row.append(total[unit_field.label])
            else:
                row.append(f"{total[field.label]:.1f}")

        rows.append(row)

        self.print(tabulate(rows, headers=headers))

    def dispatch(self, text):
        parsed = app_parser.parseString(text)

        if parsed.register:
            if name := parsed.component:
                self.register(name)
            else:
                self.print("Component name must be set")

        elif parsed.delete:
            if name := parsed.component:
                self.delete(name)
            else:
                self.print("Component name must be set")
        else:
            components = self.compute_components(parsed.components)

            if not components:
                self.print("At least one component must be set")

                return

            component = sum(components[1:], start=deepcopy(components)[0])
            component.name = parsed.assign

            if parsed.assign:
                component.kind = self._get_kind(default=component.kind)
                component.units = self._get_units(default=component.units)

                try:
                    self.repo.update(component)

                    self.print(f"Updated: {component.name}")
                except ComponentDoesNotExist:
                    self.repo.create(component)

                    self.print(f"Created: {component.name}")
                    self.reset_completer()

            elif parsed.display:
                self.display(component)

            elif parsed.detail:
                self.display_details(component, components)
