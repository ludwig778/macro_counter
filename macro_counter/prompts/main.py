from pprint import pprint as pp

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
            "+", "%", "*", "/", "=", *state.components, "delete", "register", "update", "quit"
        ])

    def dispatch(self, text):
        print()
        print("=====", text)
        parsed = PLAN_PARSER.parseString(text)
        pp(dict(parsed))

        if value := parsed.delete:
            component = Component.get(value)
            component.delete()

            state.components.pop(value, None)
            print(f"Component {value} deleted")

        elif value := parsed.register:
            print(f"REGISTER {value}")
            self.register(value)
        elif value := parsed.update:
            print(f"UPDATE {value}")
        else:
            if parsed.assign:
                print(f"ASSIGN TO {value}")
            else:
                print("SHOW COMPONENTS")

            compound = self.parse_components(parsed.components)
            print("COMPOUND")
            pp(compound.members)
            pp(compound.sum())
            display(compound)

    @staticmethod
    def parse_components(components):
        list_component = ComponentList()

        for component_data in components:
            print("====", end="")
            print(dict(component_data))

            component = component_data.get("component")

            if not (
                component and
                (component := state.components.get(component.lower()))
            ):
                print("no component, skip")
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

    def register(self, name):
        name = name.lower()

        print("Registering", name)

        attrs = {}

        ingr_kind = self.prompt("Type (L)iquid/(S)olid : ")

        if ingr_kind.lower() == "l":
            kind = "liquid"
        elif ingr_kind.lower() == "s":
            kind = "solid"
        else:
            print(f"Wrong kind : {kind}")
            return

        for k, v in fields.items():
            value = self.prompt(f"How much {v.get('name')} : ")

            if value:
                value = float(eval(value))

                attrs[k] = value

        units = attrs.pop("units", None)

        assert units, "Units must be set"

        if component := state.components.get(name.lower()):
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
            state.components[name] = component

            print(f"Creating {name}")

        print(f"Registered {name}")
