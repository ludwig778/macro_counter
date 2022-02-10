from pyparsing import (
    CaselessLiteral,
    Empty,
    Group,
    Optional,
    Suppress,
    Word,
    ZeroOrMore,
    alphas,
    delimitedList,
    nums,
)

integer = Word(nums)
float_num = Word(nums + ".")
component = Word(alphas + nums + "_")("component")

"""
COMPONENT_PARSER = Word(alphas + nums + "_")("component")

VALIDATED_COMPONENT_PARSER = (
    COMPONENT_PARSER
    #.setParseAction(validate_component)
)
"""

normalization = Suppress("%") + float_num("normalization").setParseAction(
    lambda *args: float(args[2][0])
)

operations = Group(
    (
        CaselessLiteral("*").setParseAction(lambda: "multiply")
        | CaselessLiteral("/").setParseAction(lambda: "divide")
    )("op")
    + float_num("number").setParseAction(lambda *args: float(args[2][0]))
).setResultsName("operations", listAllMatches=True)

modifiers = ZeroOrMore(normalization | operations)

component_group = delimitedList(
    Group(ZeroOrMore(component("name") + Optional(modifiers))), delim="+"
)("components")

app_parser = (
    Suppress("register")("register").setParseAction(lambda: True) + Optional(component)
    | Suppress("delete")("delete").setParseAction(lambda: True) + Optional(component)
    | component("assign") + Suppress("=") + component_group
    | Suppress("detail")("detail").setParseAction(lambda: True) + component_group
    | Empty()("display").setParseAction(lambda: True) + Optional(component_group)
)
