from macro_counter.prompts.validator import validate_ingredient

from pyparsing import (CaselessLiteral, Group, Optional, Word,
                       ZeroOrMore, OneOrMore, alphas, delimitedList, nums)


alpha = Word(alphas)
integer = Word(nums)
float_num = Word(nums + ".")


INGREDIENT_PARSER = (
    alpha("ingredient")
    .setParseAction(validate_ingredient)
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
    INGREDIENT_PARSER +
    Optional(MODIFIERS_PARSER)
)), delim="+")
