from tabulate import tabulate

from macro_counter.ingredients.base import BaseIngredient, IngredientList
from macro_counter.ingredients.fields import fields


def display(obj):
    data_array = []

    if isinstance(obj, IngredientList):
        obj_attrs = obj.sum()

    elif isinstance(obj, BaseIngredient):
        obj_attrs = obj.attrs

        data_array.append(["", obj.name])
        data_array.append(["Units", obj.units])
    else:
        raise Exception("Error")

    max_macros = sum([
        obj_attrs.get(field_name, 0.0)
        for field_name, field_data in fields.items()
        if field_data.get("macro")
    ])

    for field_name, field_data in fields.items():
        ingr_attr_value = obj_attrs.get(field_name)

        if ingr_attr_value:
            if field_data.get("show_percents") is True:
                percentage = ingr_attr_value / max_macros * 100
            else:
                percentage = None

            data_array.append([
                ("- " if field_data.get("macro") is False else "") + field_data.get("name"),
                f"{ingr_attr_value:>.1f}",
                f"{percentage:>.1f}%" if percentage else ""
            ])

    print(tabulate(data_array))
