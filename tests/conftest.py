from pytest import fixture

from macro_counter.adapters import get_adapters
from macro_counter.core.settings import get_settings
from macro_counter.repositories.components import component_repository_factory


@fixture(scope="function")
def adapters(monkeypatch):
    yield get_adapters()


@fixture(scope="function")
def failing_mongo_settings(monkeypatch):
    def get_mocked_settings():
        settings = get_settings()

        settings.mongo_settings.host = "fake.cluster"

        return settings

    monkeypatch.setattr("macro_counter.adapters.get_settings", get_mocked_settings)


@fixture(scope="function")
def incomplete_mongo_settings(monkeypatch):
    def get_mocked_settings():
        settings = get_settings()

        settings.mongo_settings.host = None

        return settings

    monkeypatch.setattr("macro_counter.adapters.get_settings", get_mocked_settings)


@fixture(scope="function")
def local_repository(adapters):
    file_adapter = adapters.file
    repo = component_repository_factory(file_adapter)(file_adapter)

    repo.delete_all()

    yield repo

    repo.delete_all()

    file_adapter.delete()


@fixture(scope="function")
def mongo_repository(adapters):
    mongo_adapter = adapters.mongo
    repo = component_repository_factory(mongo_adapter)(mongo_adapter)

    repo.delete_all()

    yield repo

    repo.delete_all()
