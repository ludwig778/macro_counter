from tabulate import tabulate

from macro_counter.fields import fields
from macro_counter.models import Component, ComponentList


def _get_field_name(field):
    return (
        fields.get(field).get("shortname") or
        fields.get(field).get("name")
    )


def _get_members(obj, cached=None):
    members = []

    for name, units in obj.components.items():
        if (
            cached and (
                member := cached.get(name)
            ) or
            (
                member := Component.get(name)
            )
        ):
            members.append(member % units)
        else:
            print(f"Couldn't find {name}")

    return members


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


def display_details(obj, cached=None):

    display(obj)

    if isinstance(obj, ComponentList):
        if len(obj.members) == 1:
            obj = obj.members[0]

            sum_attrs = {
                "units": obj.units,
                **obj.attrs
            }
            members = _get_members(obj, cached=cached)
        else:
            sum_attrs = obj.sum()
            members = obj.members

    elif isinstance(obj, Component):
        sum_attrs = obj.attrs

        if obj.components:
            members = _get_members(obj, cached=cached)

        else:
            return

    else:
        raise Exception("Error")

    data_array = []

    unit_field = _get_field_name("units")

    for member in members:
        main_data = {
            "name": member.name,
            unit_field: f"{((member.units / sum_attrs.get('units')) * 100):.1f}%"
        }
        raw_data = {
            unit_field: f"{member.units:2f}{member.measure}"
        }

        for field, field_data in fields.items():
            attr = member.attrs.get(field)

            if attr:
                field_name = _get_field_name(field)

                main_data[field_name] = f"{((attr / sum_attrs.get(field)) * 100):.1f}%"
                raw_data[field_name] = f"{attr:.1f}"

        data_array += [main_data, raw_data, {}]

    print()

    print(tabulate(data_array, headers="keys"))
