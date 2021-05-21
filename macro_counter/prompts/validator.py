from macro_counter.prompts.state import state

from pyparsing import ParseFatalException


def handle_parser_exception(func):
    def wrapper(string, loc, expr):
        try:
            func(string, loc, expr)
        except Exception as exc:
            raise ParseFatalException(string, loc, str(exc))
    return wrapper


@handle_parser_exception
def validate_component(string, loc, expr):
    name = expr[0]
    assert state.components.get(name), f"Component {name} is not registered"
