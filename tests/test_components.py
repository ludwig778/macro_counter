from pytest import mark, raises

from macro_counter.models import Component, ComponentKind, Field


@mark.parametrize(
    "kwargs",
    [
        {"label": "kcal", "fullname": "Calories"},
        {"label": "protein", "fullname": "Protein", "shortname": "Prot"},
        {"label": "carb", "fullname": "Carb", "macro": True},
        {"label": "fat", "fullname": "Fat", "show_percents": True},
    ],
)
def test_field_model(kwargs):
    assert Field(**kwargs)


@mark.parametrize(
    "kwargs",
    [
        {"name": "Butter", "kind": "solid", "units": 100, "attrs": {"fat": 23.4}},
        {"name": "Tomato", "kind": "solid", "units": 56, "attrs": {"fiber": 13}},
        {"name": "Milk", "kind": "liquid", "units": 100, "attrs": {"fat": 12.3}},
        {"name": "Coca", "kind": "liquid", "units": 100, "attrs": {"sugar": 50}},
    ],
)
def test_component_model(kwargs):
    assert Component(**kwargs)


def test_component_model_with_kind_enum():
    assert Component(name="Apple", kind=ComponentKind.SOLID)
    assert Component(name="Vodka", kind=ComponentKind.LIQUID)


def test_component_model_wrong_kind_exception():
    with raises(ValueError):
        Component(name="Vodka", kind="GASEOUS")
