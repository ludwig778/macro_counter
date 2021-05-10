from pytest import fixture

from macro_counter.repository.mongo import ingredient_collection


@fixture(autouse=True, scope="package")
def cleanup_mongo_repo():
    ingredient_collection.drop()

    yield

    ingredient_collection.drop()
