from prompt_toolkit.completion import WordCompleter

from macro_counter.ingredients import (LiquidIngredient, SolidIngredient,
                                       ingredients)
from macro_counter.ingredients.fields import fields
from macro_counter.prompts.base import BasePrompt
from macro_counter.settings import PROMPT_BASE_NAME


class RegisterPrompt(BasePrompt):
    PROMPT = f"({PROMPT_BASE_NAME}:register) => "

    def _get_completer(self):
        return WordCompleter([*ingredients.keys(), "quit"])

    def process(self, string):
        if not string:
            return
        elif string == "quit":
            return False
        elif string in ingredients:
            print(f"UPDATING {string}")
            name = string
        else:
            print(f"CREATING {string}")
            name = string

        attrs = {}

        fullname = self.session.prompt("Name : ")

        ingr_kind = self.session.prompt("Type (L)iquid/(S)olid : ")
        if ingr_kind.lower() == "l":
            attrs["kind"] = "Liquid"
            ingredient_class = LiquidIngredient
        elif ingr_kind.lower() == "s":
            attrs["kind"] = "Solid"
            ingredient_class = SolidIngredient
        else:
            print(f"Wrong kind : {ingr_kind}")
            return

        for k, v in fields.items():

            value = self.session.prompt(f"How much {v.get('name')} : ")

            if value:
                value = float(eval(value))

                attrs[k] = value

        ingredients[name] = ingredient_class(fullname, **attrs)

        print(f"Registered {name}")
