from pyparsing import (CaselessLiteral, Group, OneOrMore, Optional, Word,
                       ZeroOrMore, alphas, delimitedList, nums, printables)

from macro_counter.prompts.validator import validate_component

integer = Word(nums)
float_num = Word(nums + ".")


COMPONENT_PARSER = (
    Word(printables)("component")
    .setParseAction(validate_component)
)

CALIBRATION_PARSER = (
    CaselessLiteral("%").suppress() +
    float_num("calibration").setParseAction(lambda *args: float(args[2][0]))
)

OPERATION_PARSER = (
    (
        CaselessLiteral("*") |
        CaselessLiteral("/")
    ).setResultsName("operations", listAllMatches=True) +
    float_num
    .setResultsName("numbers", listAllMatches=True)
    .setParseAction(lambda *args: float(args[2][0]))
)

MODIFIERS_PARSER = (
    Optional(CALIBRATION_PARSER) +
    ZeroOrMore(OPERATION_PARSER)
)

PLAN_PARSER = delimitedList(Group(OneOrMore(
    COMPONENT_PARSER +
    Optional(MODIFIERS_PARSER)
)), delim="+")
