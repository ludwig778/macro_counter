from tabulate import tabulate

from macro_counter.fields import fields
from macro_counter.models import Component, ComponentList


def display(obj):
    data_array = []

    if isinstance(obj, ComponentList):
        obj_attrs = obj.sum()

        if all(map(lambda m: m.kind == "liquid", obj.members)):
            measure = "ml"
        else:
            measure = "mg"

    elif isinstance(obj, Component):
        obj_attrs = obj.attrs
        measure = obj.measure

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
                f"{ingr_attr_value:>.1f}" + (measure if field_name == "units" else ""),
                f"{percentage:>.1f}%" if percentage else ""
            ])

    print(tabulate(data_array))
