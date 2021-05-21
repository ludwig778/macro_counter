from pytest import mark, raises

from macro_counter.models import Component


@mark.parametrize("kwargs", [
    {"name": "Butter", "kind": "solid",  "units": 100, "attrs": {"fat": 23.4}},
    {"name": "Tomato", "kind": "solid",  "units": 56,  "attrs": {"fiber": 13}},
    {"name": "Milk",   "kind": "liquid", "units": 100, "attrs": {"fat": 12.3}},
    {"name": "Coca",   "kind": "liquid", "units": 100, "attrs": {"sugar": 50}},
])
def test_create_components(kwargs):
    Component.create(**kwargs)


def test_create_components_exception():
    with raises(Exception, match="Kind must be set"):
        Component.create("Vodka")


def test_list_components():
    assert len(Component.list()) == 4
    assert len(Component.list(kind="liquid")) == 2
    assert len(Component.list(kind="solid")) == 2


@mark.parametrize("name", [
    "Coca", "Tomato"
])
def test_get_component(name):
    assert Component.get(name)


def test_get_non_existing_component():
    assert Component.get("TEST") is None


def test_updating_component():
    brown_sugar = Component.create("brown_sugar", kind="solid", units=100)

    old_units = brown_sugar.units

    brown_sugar.update(units=200)

    new_units = brown_sugar.units

    assert old_units != new_units


def test_deleting_component():
    brown_sugar = Component.get("brown_sugar")

    brown_sugar.delete()

    assert Component.get("brown_sugar") is None


def test_multiplicating_component():
    tomato = Component.get("Tomato")

    assert (tomato * 10).to_dict() == {
        "name": "Tomato",
        "kind": "solid",
        "units": 560,
        "attrs": {
            "fiber": 130
        }
    }


def test_normalize_component():
    tomato = Component.get("Tomato")

    assert (tomato % 28).to_dict() == {
        "name": "Tomato",
        "kind": "solid",
        "units": 28.0,
        "attrs": {
            "fiber": 6.499999999999999
        }
    }
