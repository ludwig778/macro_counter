from prompt_toolkit.completion import WordCompleter

from .base import BasePrompt
from .plan import PlanPrompt
from .register import RegisterPrompt
from .settings import PROMPT_BASE_NAME


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
