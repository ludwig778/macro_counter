from prompt_toolkit import PromptSession


class BasePrompt(object):
    PROMPT = None

    def __init__(self):
        self.session = PromptSession(
            completer=self._get_completer()
        )

    def _get_completer(self):
        raise NotImplementedError

    def loop(self):
        while True:
            try:
                text = self.session.prompt(self.PROMPT)
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.

            text = text.strip()

            if self.process(text) is False:
                break

    def process(self, string):
        raise NotImplementedError
