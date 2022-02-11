from pytest import fixture, mark

from macro_counter.app.prompt import AppPrompt as MainPrompt
from macro_counter.app.prompt import PromptState
from macro_counter.models import Component, ComponentKind


@fixture(autouse=True)
def seed_mongo(mongo_repository):
    for component in [
        Component(
            name="Tomato_100gr",
            kind=ComponentKind.SOLID,
            units=100.0,
            attrs={
                "kcal": 18.0,
                "protein": 0.9,
                "carb": 3.9,
                "sugar": 2.6,
                "fiber": 1.2,
                "fat": 0.2,
            },
        ),
        Component(
            name="Mozzarella_100gr",
            kind=ComponentKind.SOLID,
            units=100.0,
            attrs={
                "kcal": 259.0,
                "protein": 19.9,
                "carb": 2.2,
                "sugar": 0.4,
                "fat": 19.4,
                "saturated_fat": 12.3,
                "mono_fat": 5.3,
                "poly_fat": 0.6,
            },
        ),
        Component(
            name="Orange_Juice_100ml",
            kind=ComponentKind.LIQUID,
            units=100.0,
            attrs={
                "kcal": 110.0,
                "protein": 2.0,
                "carb": 27.0,
                "sugar": 20.0,
                "fiber": 1.0,
            },
        ),
    ]:
        mongo_repository.create(component)


@fixture(autouse=True, scope="function")
def prompt_redirect(monkeypatch):
    def input_generator(inputs):
        for input in inputs:
            yield input

        raise EOFError()

    class Redirect:
        def __init__(self):
            self.inputs = input_generator([])
            self.outputs = []

        def set_inputs(self, *inputs):
            self.inputs = input_generator(inputs)

        def add_output(self, output, **kwargs):
            self.outputs += [output]

        def send_input(self, text=None, **kwargs):
            next_input = next(self.inputs)

            self.add_output(f"{text or ''}{next_input}")

            return next_input

    redirect = Redirect()

    monkeypatch.setattr(
        "macro_counter.app.prompt.AppPrompt.prompt", redirect.send_input
    )
    monkeypatch.setattr("macro_counter.app.prompt.AppPrompt.print", redirect.add_output)

    return redirect


def test_prompt_stopped_state():
    prompt = MainPrompt()
    prompt.loop()

    assert prompt.state is PromptState.STOPPED


def test_prompt_message(prompt_redirect):
    prompt_redirect.set_inputs("")

    MainPrompt().loop()

    assert ">>> " in prompt_redirect.outputs


@mark.parametrize("input", ["q", "quit"])
def test_prompt_quit(input, prompt_redirect):
    prompt_redirect.set_inputs(input)

    MainPrompt().loop()

    assert "quitting..." in prompt_redirect.outputs


@mark.parametrize("input", ["l", "leave"])
def test_prompt_leave(input, prompt_redirect):
    prompt_redirect.set_inputs(input)

    MainPrompt().loop()

    assert "leaving..." in prompt_redirect.outputs


def test_prompt_delete_component(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs("delete Tomato_100gr")

    MainPrompt().loop()

    assert len(mongo_repository.list()) == 2
    assert "Component Tomato_100gr deleted" in prompt_redirect.outputs


def test_prompt_delete_component_raise_without_name(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs("delete")

    MainPrompt().loop()

    assert "Component name must be set" in prompt_redirect.outputs


def test_prompt_delete_component_does_not_exist_exception(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs("delete Bread")

    MainPrompt().loop()

    assert "Component Bread not found" in prompt_redirect.outputs


def test_prompt_register_component(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs(
        "register Bread",
        "Solid",  # Set kind
        "100",  # units
        "77",  # kcal
        "2.6",  # protein
        "14",  # carb
        "0.8",  # fiber
        "1.6",  # sugar
        "1",  # fat
        "0.2",  # sat fat
        "0.2",  # mono fat
        "0.5",  # poly fat
        "0.1",  # trans fat
    )

    MainPrompt().loop()

    bread = mongo_repository.get("Bread")

    assert bread.dict() == {
        "name": "Bread",
        "kind": ComponentKind.SOLID,
        "units": 100.0,
        "attrs": {
            "kcal": 77.0,
            "protein": 2.6,
            "carb": 14.0,
            "fiber": 0.8,
            "sugar": 1.6,
            "fat": 1.0,
            "saturated_fat": 0.2,
            "mono_fat": 0.2,
            "poly_fat": 0.5,
            "trans_fat": 0.1,
        },
    }


def test_prompt_register_component_using_default_values(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "register Coke",
        "liquid",  # Set kind
        "",  # units
        "",  # kcal
        "",  # protein
        "",  # carb
        "",  # fiber
        "",  # sugar
        "",  # fat
        "",  # sat fat
        "",  # mono fat
        "",  # poly fat
        "",  # trans fat
    )

    MainPrompt().loop()

    coke = mongo_repository.get("Coke")

    assert coke.dict() == {
        "name": "Coke",
        "kind": ComponentKind.LIQUID,
        "units": 100.0,
        "attrs": {},
    }
    assert "Type units (100.0) : " in prompt_redirect.outputs


def test_prompt_register_component_raise_without_name(prompt_redirect):
    prompt_redirect.set_inputs("register")

    MainPrompt().loop()

    assert "Component name must be set" in prompt_redirect.outputs


def test_prompt_register_component_raise_wrong_kind(prompt_redirect):
    prompt_redirect.set_inputs("register Coke", "")  # kind

    MainPrompt().loop()

    assert "Error: Wrong kind" in prompt_redirect.outputs


def test_prompt_register_component_raise_wrong_units(prompt_redirect):
    prompt_redirect.set_inputs("register Coke", "solid", "TEST")  # kind  # units

    MainPrompt().loop()

    assert "Error: Wrong value, number required" in prompt_redirect.outputs


def test_prompt_register_component_raise_wrong_attribute(prompt_redirect):
    prompt_redirect.set_inputs(
        "register Coke", "solid", "100", "TEST"  # kind  # units  # kcal
    )

    MainPrompt().loop()

    assert "Error: Wrong value, number required" in prompt_redirect.outputs


def test_prompt_update_component(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs(
        "register Tomato_100gr",
        "Liquid",  # Set kind
        "123",  # units, testing value
        "20.0",  # kcal
        "1.0",  # protein
        "4.1",  # carb
        "",  # fiber
        "",  # sugar
        "reset",  # fat
        "",  # sat fat
        "",  # mono fat
        "",  # poly fat
        "",  # trans fat
    )

    MainPrompt().loop()

    component = mongo_repository.get("Tomato_100gr")

    assert component.dict() == {
        "name": "Tomato_100gr",
        "kind": ComponentKind.LIQUID,
        "units": 123.0,
        "attrs": {
            "kcal": 20.0,
            "protein": 1.0,
            "carb": 4.1,
            "sugar": 2.6,
            "fiber": 1.2,
        },
    }


def test_prompt_update_component_when_nothing_changed(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "register Tomato_100gr",
        "",  # Set kind
        "",  # units, testing value
        "",  # kcal
        "",  # protein
        "",  # carb
        "",  # fiber
        "",  # sugar
        "",  # fat
        "",  # sat fat
        "",  # mono fat
        "",  # poly fat
        "",  # trans fat
    )

    MainPrompt().loop()

    assert "Nothing changed" in prompt_redirect.outputs


def test_prompt_update_component_raise_wront_value(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs(
        "register Tomato_100gr",
        "",  # Set kind
        "",  # units
        "test",  # wrong entry
    )

    MainPrompt().loop()

    assert "Error: Wrong value, number required" in prompt_redirect.outputs


def test_prompt_direct_component_assignment(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs(
        "New_Tomato_100gr = Tomato_100gr",
        "",  # kind
        "",  # units
    )

    MainPrompt().loop()

    base = mongo_repository.get("Tomato_100gr")
    assigned = mongo_repository.get("New_Tomato_100gr")

    assert base.kind == assigned.kind
    assert base.units == assigned.units == 100
    assert base.attrs == assigned.attrs


def test_prompt_direct_component_assignment_with_update(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "Dried_Tomato_50gr = Tomato_100gr",
        "",  # kind
        "50",  # units
    )

    MainPrompt().loop()

    base = mongo_repository.get("Tomato_100gr")
    assigned = mongo_repository.get("Dried_Tomato_50gr")

    assert base.kind == assigned.kind
    assert assigned.units == 50
    assert base.attrs == assigned.attrs


def test_prompt_direct_component_assignment_raise_without_components(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs("New_Tomato_100gr = ")

    MainPrompt().loop()

    assert "At least one component must be set" in prompt_redirect.outputs


def test_prompt_direct_component_assignment_raise_with_unknown_components(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs("Smoothie_red_100gr = Raspberry + Blueberry + Water")

    MainPrompt().loop()

    assert prompt_redirect.outputs == [
        "Using mongo store",
        ">>> Smoothie_red_100gr = Raspberry + Blueberry + Water",
        "No component Raspberry has been found: skipping",
        "No component Blueberry has been found: skipping",
        "No component Water has been found: skipping",
        "At least one component must be set",
        "EOF : quitting...",
    ]


def test_prompt_component_assignation_with_calibration_op(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "Tomato_33gr = Tomato_100gr % 33",
        "",  # kind
        "",  # units
    )

    MainPrompt().loop()

    base = mongo_repository.get("Tomato_100gr")
    assigned = mongo_repository.get("Tomato_33gr")

    base = base % 33

    assert base.kind == assigned.kind
    assert base.units == assigned.units == 33
    assert base.attrs == assigned.attrs


def test_prompt_component_assignation_with_multiplication_op(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "Tomato_200gr = Tomato_100gr * 2",
        "",  # kind
        "",  # units
    )

    MainPrompt().loop()

    base = mongo_repository.get("Tomato_100gr")
    assigned = mongo_repository.get("Tomato_200gr")

    base = base * 2

    assert base.kind == assigned.kind
    assert base.units == assigned.units == 200
    assert base.attrs == assigned.attrs


def test_prompt_component_assignation_with_division_op(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "Tomato_50gr = Tomato_100gr / 2",
        "",  # kind
        "",  # units
    )

    MainPrompt().loop()

    base = mongo_repository.get("Tomato_100gr")
    assigned = mongo_repository.get("Tomato_50gr")

    base = base / 2

    assert base.kind == assigned.kind
    assert base.units == assigned.units == 50
    assert base.attrs == assigned.attrs


def test_prompt_component_assignation_with_multiple_operations(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "Tomato_125gr = Tomato_100gr % 50 * 5 / 2",
        "",  # kind
        "",  # units
    )

    MainPrompt().loop()

    base = mongo_repository.get("Tomato_100gr")
    assigned = mongo_repository.get("Tomato_125gr")

    base = base % 50 * 5 / 2

    assert base.kind == assigned.kind
    assert base.units == assigned.units == 125
    assert base.attrs == assigned.attrs


def test_prompt_multiple_component_assignment(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs(
        "Tomato_Salad_200gr = Tomato_100gr + Mozzarella_100gr", "", ""  # kind  # units
    )

    MainPrompt().loop()

    component = mongo_repository.get("Tomato_Salad_200gr")

    assert component.dict() == {
        "name": "Tomato_Salad_200gr",
        "kind": ComponentKind.SOLID,
        "units": 200.0,
        "attrs": {
            "kcal": 277.0,
            "protein": 20.799999999999997,
            "carb": 6.1,
            "fiber": 1.2,
            "sugar": 3.0,
            "fat": 19.599999999999998,
            "saturated_fat": 12.3,
            "mono_fat": 5.3,
            "poly_fat": 0.6,
        },
    }


def test_prompt_multiple_component_assignment_with_some_operations(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "Light_Tomato_Salad_250gr = Tomato_100gr * 2 + Mozzarella_100gr % 50",
        "",  # kind
        "",  # units
    )

    MainPrompt().loop()

    component = mongo_repository.get("Light_Tomato_Salad_250gr")

    assert component.dict() == {
        "name": "Light_Tomato_Salad_250gr",
        "kind": ComponentKind.SOLID,
        "units": 250.0,
        "attrs": {
            "kcal": 165.5,
            "protein": 11.75,
            "carb": 8.9,
            "fiber": 2.4,
            "sugar": 5.4,
            "fat": 10.1,
            "saturated_fat": 6.15,
            "mono_fat": 2.65,
            "poly_fat": 0.3,
        },
    }


def test_prompt_multiple_component_assignment_with_some_overriding(
    prompt_redirect, mongo_repository
):
    prompt_redirect.set_inputs(
        "Blended_Tomato_Mozza_300gr = Tomato_100gr + Mozzarella_100gr",
        "Liquid",  # kind
        "300",  # units
    )

    MainPrompt().loop()

    component = mongo_repository.get("Blended_Tomato_Mozza_300gr")

    assert component.dict() == {
        "name": "Blended_Tomato_Mozza_300gr",
        "kind": ComponentKind.LIQUID,
        "units": 300.0,
        "attrs": {
            "kcal": 277.0,
            "protein": 20.799999999999997,
            "carb": 6.1,
            "fiber": 1.2,
            "sugar": 3.0,
            "fat": 19.599999999999998,
            "saturated_fat": 12.3,
            "mono_fat": 5.3,
            "poly_fat": 0.6,
        },
    }


def test_prompt_show_single_component(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs("Orange_Juice_100ml")

    MainPrompt().loop()

    assert prompt_redirect.outputs == [
        "Using mongo store",
        ">>> Orange_Juice_100ml",
        "--------  --------  -----\n"
        "Calories  110.0\n"
        "Units     100.0 ml\n"
        "Protein   2.0       6.9%\n"
        "Carb      27.0      93.1%\n"
        "Fiber     1.0\n"
        "- Sugar   20.0      69.0%\n"
        "--------  --------  -----",
        "EOF : quitting...",
    ]


def test_prompt_show_summed_multiple_component(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs("Tomato_100gr + Mozzarella_100gr")

    MainPrompt().loop()

    assert prompt_redirect.outputs == [
        "Using mongo store",
        ">>> Tomato_100gr + Mozzarella_100gr",
        "----------------------  --------  -----\n"
        "Calories                277.0\n"
        "Units                   200.0 gr\n"
        "Protein                 20.8      44.7%\n"
        "Carb                    6.1       13.1%\n"
        "Fiber                   1.2\n"
        "- Sugar                 3.0       6.5%\n"
        "Fat                     19.6      42.2%\n"
        "- Saturated fat         12.3      26.5%\n"
        "- Mono insaturated fat  5.3       11.4%\n"
        "- Poly insaturated fat  0.6       1.3%\n"
        "----------------------  --------  -----",
        "EOF : quitting...",
    ]


def test_prompt_show_detailed_multiple_component(prompt_redirect, mongo_repository):
    prompt_redirect.set_inputs("detail Tomato_100gr + Mozzarella_100gr * 2")

    MainPrompt().loop()

    assert prompt_redirect.outputs == [
        "Using mongo store",
        ">>> detail Tomato_100gr + Mozzarella_100gr * 2",
        "Name              Units    Cal    Prot    Carb    Fiber    Sugar    Fat    Sat     Mono    Poly\n"
        "----------------  -------  -----  ------  ------  -------  -------  -----  ------  ------  ------\n"
        "Tomato_100gr      100.0gr  18.0   0.9     3.9     1.2      2.6      0.2\n"
        "                  33.3%    3.4%   2.2%    47.0%   100.0%   76.5%    0.5%\n"
        "Mozzarella_100gr  200.0gr  518.0  39.8    4.4              0.8      38.8   24.6    10.6    1.2\n"
        "                  66.7%    96.6%  97.8%   53.0%            23.5%    99.5%  100.0%  100.0%  100.0%\n"
        "\n"
        "Total             300.0    536.0  40.7    8.3     1.2      3.4      39.0   24.6    10.6    1.2",
        "EOF : quitting...",
    ]
