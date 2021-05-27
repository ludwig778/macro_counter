from prompt_toolkit.completion import WordCompleter

from macro_counter.display import display
from macro_counter.fields import fields
from macro_counter.models import Component, ComponentList
from macro_counter.prompts.base import BasePrompt
from macro_counter.prompts.parsers import PLAN_PARSER
from macro_counter.prompts.state import state


class MainPrompt(BasePrompt):
    PROMPT_STR = ">>> "

    def _get_completer(self):
        return WordCompleter([
            "+", "%", "*", "/", "=", *state.components, "register", "delete", "quit"
        ])

    def dispatch(self, text):
        parsed = PLAN_PARSER.parseString(text)

        if name := parsed.delete:
            name = name.lower()

            self.delete(name)

        elif name := parsed.register:
            name = name.lower()

            self.register(name)

        else:
            compound = self.parse_components(parsed.components)

            if name := parsed.assign:
                name = name.lower()

                self.assign(name, compound)

            else:
                display(compound)

    @staticmethod
    def parse_components(components):
        list_component = ComponentList()

        for component_data in components:
            component = component_data.get("component")

            if not (
                component and
                (component := state.components.get(component.lower()))
            ):
                print("No component, skip")
                continue

            calibration = component_data.get("calibration") or None
            numbers = component_data.get("numbers") or []
            operations = component_data.get("operations") or []

            base_multiplier = 1
            for num, multiplier in list(zip(numbers, operations))[::-1]:
                if multiplier == "/":
                    base_multiplier /= num
                if multiplier == "*":
                    base_multiplier *= num

            if calibration:
                component %= calibration

            if base_multiplier != 1:
                component *= base_multiplier

            list_component.append(component)

        return list_component

    def _get_units(self, default=None):
        units_raw = self.prompt(f"Type units{' (' + str(default) + ') ' if default else ''}: ")

        if units_raw:
            units = float(units_raw)
        else:
            units = default

        return units

    def _get_kind(self, default=None):
        kind_raw = self.prompt(f"Type (L)iquid/(S)olid{' (' + str(default.capitalize()) + ') ' if default else ''}: ")

        if kind_raw.lower() in ("l", "liquid"):
            kind = "liquid"
        elif kind_raw.lower() in ("s", "solid"):
            kind = "solid"
        else:
            kind = default

        return kind

    def _get_attrs(self, defaults=None):
        attrs = defaults or {}

        for k, v in fields.items():
            value = None
            if default := attrs.get(k):
                value = self.prompt(f"How much {v.get('name')} ({default}/Reset): ")
            else:
                value = self.prompt(f"How much {v.get('name')} : ")

            if value.lower() in ("r", "reset"):
                attrs.pop(k)
                value = None
            elif value:
                value = float(eval(value))
            elif default:
                value = float(default)

            if value:
                attrs[k] = value

        return attrs

    def assign(self, name, compound):
        attrs = compound.sum()
        units = attrs.pop("units")

        kind = None
        if len(compound.members) == 1:
            kind = compound.members[0].kind

        units = self._get_units(default=units)
        kind = self._get_kind(default=kind)

        component, created = self.create_or_update_component(name, kind, units, attrs)

        if created:
            state.components[name] = component
            self.reset_completer()

    def delete(self, name):
        component = Component.get(name)
        component.delete()

        state.components.pop(name, None)
        self.reset_completer()

        print(f"Component {name} deleted")

    def register(self, name):
        name = name.lower()

        component = Component.get(name)

        if not component:
            print("Registering", name)

            kind = self._get_kind()
            attrs = self._get_attrs()
        else:
            print("Updating", name)

            kind = self._get_kind(default=component.kind)
            attrs = self._get_attrs(defaults={"units": component.units, **component.attrs})

        units = attrs.pop("units", None)

        component, _ = self.create_or_update_component(
            name, kind, units, attrs,
            component=component
        )

        self.reset_completer()

    def create_or_update_component(self, name, kind, units, attrs, component=None):
        created = False

        assert units, "Units must be set"
        assert kind in ("solid", "liquid"), "Kind must be either solid or liquid"

        if component or (component := state.components.get(name.lower())):
            component.update(
                kind=kind,
                units=units,
                attrs=attrs
            )
            print(f"Updating {name}")

        else:
            component = Component.create(
                name,
                kind=kind,
                units=units,
                attrs=attrs
            )
            created = True

            print(f"Creating {name}")

        state.components[name] = component

        return component, created
