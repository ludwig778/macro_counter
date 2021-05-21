from prompt_toolkit.completion import WordCompleter

from macro_counter.display import display
from macro_counter.models import ComponentList
from macro_counter.prompts.base import BasePrompt
from macro_counter.prompts.state import state
from macro_counter.prompts.parsers import PLAN_PARSER


class PlanPrompt(BasePrompt):
    PROMPT_STR = "(plan) => "

    def _get_completer(self):
        return WordCompleter([
            "+", "%", "*", "/", *state.components, "plan", "quit"
        ])

    def dispatch(self, text):
        print()
        list_component = ComponentList()

        for component_data in PLAN_PARSER.parseString(text):

            component = component_data.get("component")
            calibration = component_data.get("calibration") or None
            numbers = component_data.get("numbers") or []
            operations = component_data.get("operations") or []

            component = state.components.get(component.lower())

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

            print(component, calibration, numbers, operations)

            display(component)
            list_component.append(component)

        display(list_component)
