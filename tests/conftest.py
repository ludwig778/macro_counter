from pathlib import Path

from hartware_lib.adapters.filesystem import DirectoryAdapter
from hartware_lib.serializers import serialize
from pytest import fixture

from macro_counter.adapters import Adapters
from macro_counter.repositories.local import LocalComponentRepository
from macro_counter.settings import AppSettings


@fixture(scope="function", autouse=True)
def clean_test_directory_():
    test_directory = DirectoryAdapter(path=Path(".testing"))
    test_directory.create()

    yield

    test_directory.delete()


@fixture(scope="function")
def settings():
    yield AppSettings.build()


@fixture(scope="function")
def adapters(settings):
    yield Adapters.build(settings)


@fixture(scope="function")
def local_repository(adapters):
    file_adapter = adapters.store_file
    file_adapter.write(serialize({}))

    repo = LocalComponentRepository(file_adapter)

    repo.delete_all()

    yield repo

    repo.delete_all()

    file_adapter.delete()
