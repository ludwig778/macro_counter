from prompt_toolkit.completion import WordCompleter

from macro_counter.ingredients import IngredientList, ingredients
from macro_counter.prompts.base import BasePrompt
from macro_counter.settings import PROMPT_BASE_NAME


class PlanPrompt(BasePrompt):
    PROMPT = f"({PROMPT_BASE_NAME}:plan) => "

    def _get_completer(self):
        return WordCompleter(["*", "+", *ingredients.keys(), "quit"])

    def process(self, string):
        if not string:
            return

        if string == "quit":
            return False

        ingr_list = IngredientList()

        for sub_string in string.split("+"):
            sub_split = list(map(str.strip, sub_string.split("*")))

            if len(sub_split) > 0:
                ingredient = ingredients.get(sub_split[0])

                if len(sub_split) > 1:
                    units = float(eval(sub_split[1]))
                    ingredient = ingredient * (units / ingredient.units)
                else:
                    units = None

            ingr_list.append(ingredient)

        from ingredients.display import display

        print()
        display(ingr_list)
        print()
