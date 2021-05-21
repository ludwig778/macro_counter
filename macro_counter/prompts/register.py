from prompt_toolkit.completion import WordCompleter

from macro_counter.models import Component
from macro_counter.fields import fields
from macro_counter.prompts.base import BasePrompt
from macro_counter.prompts.state import state


class RegisterPrompt(BasePrompt):
    PROMPT_STR = "(register) => "

    def _get_completer(self):
        return WordCompleter([*state.components, "leave", "quit"])

    def dispatch(self, name):
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
