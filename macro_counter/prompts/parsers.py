from pyparsing import (CaselessLiteral, Group, Optional, Word, ZeroOrMore,
                       alphas, delimitedList, nums)

from macro_counter.prompts.validator import validate_component

integer = Word(nums)
float_num = Word(nums + ".")
component = Word(alphas + nums + "_")


COMPONENT_PARSER = Word(alphas + nums + "_")("component")

VALIDATED_COMPONENT_PARSER = (
    COMPONENT_PARSER
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

ASSIGN_PARSER = (
    component("assign") +
    CaselessLiteral("=").suppress()
)
REGISTER_PARSER = (
    CaselessLiteral("register").suppress() +
    component("register")
)
DETAIL_PARSER = (
    CaselessLiteral("detail")("detail")
    .setParseAction(lambda *args: True)
)
DELETE_PARSER = (
    CaselessLiteral("delete") +
    VALIDATED_COMPONENT_PARSER("delete")
)

COMPONENT_GROUP_PARSER = delimitedList(
    Group(
        ZeroOrMore(
            VALIDATED_COMPONENT_PARSER +
            Optional(MODIFIERS_PARSER)
        )
    ),
    delim="+"
)("components")

PLAN_PARSER = (
    (
        ASSIGN_PARSER +
        COMPONENT_GROUP_PARSER
    ) |
    (
        DETAIL_PARSER +
        COMPONENT_GROUP_PARSER
    ) |
    REGISTER_PARSER |
    DELETE_PARSER |
    COMPONENT_GROUP_PARSER
)
