from prompt_toolkit.completion import WordCompleter

from macro_counter.prompts.base import BasePrompt, PromptSignal
from macro_counter.prompts.plan import PlanPrompt
from macro_counter.prompts.register import RegisterPrompt


class RootPrompt(BasePrompt):
    PROMPT_STR = ">>> "

    def _get_completer(self):
        return WordCompleter(["register", "plan", "quit"])

    def dispatch(self, text):
        signal = None

        if text in ("plan", "p"):
            signal = PlanPrompt().loop()

        elif text in ("register", "r"):
            signal = RegisterPrompt().loop()

        if signal == PromptSignal.QUIT:
            return PromptSignal.QUIT
