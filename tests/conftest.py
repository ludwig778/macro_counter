from pytest import fixture

from macro_counter.repository import mongo_repo


@fixture(autouse=True, scope="package")
def cleanup_mongo_repo():
    mongo_repo.drop("component")

    yield

    mongo_repo.drop("component")
