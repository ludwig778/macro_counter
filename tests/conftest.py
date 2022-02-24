from pathlib import Path

from hartware_lib.adapters.directory import DirectoryAdapter
from pytest import fixture

from macro_counter.adapters import get_adapters
from macro_counter.core.settings import get_settings
from macro_counter.repositories.components import component_repository_factory


@fixture(scope="function", autouse=True)
def clean_test_directory_():
    test_directory = DirectoryAdapter(dir_path=Path(".testing"))
    test_directory.create()

    yield

    test_directory.delete()


@fixture(scope="function")
def adapters():
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
    file_adapter = adapters.local_store
    file_adapter.write_json({})

    repo = component_repository_factory(file_adapter)

    repo.delete_all()

    yield repo

    repo.delete_all()

    file_adapter.delete()


@fixture(scope="function")
def mongo_repository(adapters):
    mongo_adapter = adapters.mongo
    repo = component_repository_factory(mongo_adapter)

    repo.delete_all()

    yield repo

    repo.delete_all()
