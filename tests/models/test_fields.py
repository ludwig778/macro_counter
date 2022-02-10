from pytest import mark

from macro_counter.models import Field


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
