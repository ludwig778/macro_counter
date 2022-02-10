from pytest import fixture, raises

from macro_counter.exceptions import ComponentAlreadyExist, ComponentDoesNotExist
from macro_counter.models import Component, ComponentKind


@fixture(autouse=True)
def seed_mongo(mongo_repository):
    for component in [
        Component(name="Tomato", kind=ComponentKind.SOLID),
        Component(name="Cheese", kind=ComponentKind.SOLID),
        Component(name="Coco_Milk", kind=ComponentKind.LIQUID),
    ]:
        mongo_repository.create(component)


def test_mongo_repository_create_component(mongo_repository):
    assert mongo_repository.create(Component(name="Ham", kind=ComponentKind.SOLID))

    assert len(mongo_repository.list()) == 4


def test_mongo_repository_create_component_already_exist_exception(mongo_repository):
    with raises(ComponentAlreadyExist):
        mongo_repository.create(Component(name="Tomato", kind=ComponentKind.SOLID))


def test_mongo_repository_update_component(mongo_repository):
    updated = mongo_repository.update(
        Component(name="Tomato", kind=ComponentKind.SOLID, units=123.0)
    )
    assert updated.units == 123.0


def test_mongo_repository_update_component_does_not_exist_exception(mongo_repository):
    with raises(ComponentDoesNotExist):
        mongo_repository.update(
            Component(
                name="Cream_Cheese", kind=ComponentKind.SOLID, attrs={"fat": 33.0}
            )
        )


def test_mongo_repository_get_components(mongo_repository):
    assert mongo_repository.get("Tomato")


def test_mongo_repository_get_component_does_not_exist_exception(mongo_repository):
    with raises(ComponentDoesNotExist):
        assert mongo_repository.get("Avocado")


def test_mongo_repository_list_components(mongo_repository):
    assert len(mongo_repository.list()) == 3


def test_mongo_repository_delete_components(mongo_repository):
    component = mongo_repository.get("Tomato")

    assert mongo_repository.delete(component)

    assert len(mongo_repository.list()) == 2


def test_mongo_repository_delete_component_does_not_exist_exception(mongo_repository):
    scoped_component = Component(name="Strawberry", kind=ComponentKind.SOLID)

    with raises(ComponentDoesNotExist):
        assert mongo_repository.delete(scoped_component)


def test_mongo_repository_delete_all_components(mongo_repository):
    mongo_repository.delete_all()

    assert mongo_repository.list() == []
