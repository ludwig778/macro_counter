from prompt_toolkit.completion import WordCompleter

from prompts.base import BasePrompt
from prompts.plan import PlanPrompt
from prompts.register import RegisterPrompt
from prompts.settings import PROMPT_BASE_NAME


class MainPrompt(BasePrompt):
    PROMPT = f"({PROMPT_BASE_NAME}) => "

    def _get_completer(self):
        return WordCompleter(["register", "plan", "quit"])

    def process(self, string):
        if not string:
            return
        elif string == "quit":
            return False
        elif string == "plan":
            return PlanPrompt().loop()
        elif string == "register":
            return RegisterPrompt().loop()
