from pytest import fixture, raises

from macro_counter.exceptions import ComponentAlreadyExist, ComponentDoesNotExist
from macro_counter.models import Component, ComponentKind


@fixture(autouse=True)
def seed_local(local_repository):
    for component in [
        Component(name="Tomato", kind=ComponentKind.SOLID),
        Component(name="Cheese", kind=ComponentKind.SOLID),
        Component(name="Coco_Milk", kind=ComponentKind.LIQUID),
    ]:
        local_repository.create(component)


def test_local_repository_create_component(local_repository):
    assert local_repository.create(Component(name="Ham", kind=ComponentKind.SOLID))

    assert len(local_repository.list()) == 4


def test_local_repository_create_component_already_exist_exception(local_repository):
    with raises(ComponentAlreadyExist):
        local_repository.create(Component(name="Tomato", kind=ComponentKind.SOLID))


def test_local_repository_update_component(local_repository):
    updated = local_repository.update(
        Component(name="Tomato", kind=ComponentKind.SOLID, units=123.0)
    )
    assert updated.units == 123.0


def test_local_repository_update_component_does_not_exist_exception(local_repository):
    with raises(ComponentDoesNotExist):
        local_repository.update(
            Component(
                name="Cream_Cheese", kind=ComponentKind.SOLID, attrs={"fat": 33.0}
            )
        )


def test_local_repository_get_components(local_repository):
    assert local_repository.get("Tomato")


def test_local_repository_get_component_does_not_exist_exception(local_repository):
    with raises(ComponentDoesNotExist):
        assert local_repository.get("Avocado")


def test_local_repository_list_components(local_repository):
    assert len(local_repository.list()) == 3


def test_local_repository_delete_components(local_repository):
    component = local_repository.get("Tomato")

    assert local_repository.delete(component)

    assert len(local_repository.list()) == 2


def test_local_repository_delete_component_does_not_exist_exception(local_repository):
    scoped_component = Component(name="Strawberry", kind=ComponentKind.SOLID)

    with raises(ComponentDoesNotExist):
        assert local_repository.delete(scoped_component)


def test_local_repository_delete_all_components(local_repository):
    local_repository.delete_all()

    assert local_repository.list() == []
