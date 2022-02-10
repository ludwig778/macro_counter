from pathlib import Path
from shutil import rmtree

from pytest import fixture

# from macro_counter.repositories.components.factory import repository_factory
from macro_counter.adapters.file import FileAdapter
from macro_counter.adapters.mongo import MongoAdapter
from macro_counter.core.settings import get_settings
from macro_counter.repositories.components import component_repository_factory


@fixture(scope="function")
def local_repository():
    local_path = Path().home() / ".testing" / "local_store.json"
    file_adapter = FileAdapter(local_path)
    file_adapter.create()

    repo = component_repository_factory(file_adapter)(file_adapter)

    repo.delete_all()

    yield repo

    repo.delete_all()

    file_adapter.delete()
    rmtree(file_adapter.path.parent)


@fixture(scope="function")
def mongo_repository():
    settings = get_settings()
    mongo_adapter = MongoAdapter(settings.mongo_settings)

    repo = component_repository_factory(mongo_adapter)(mongo_adapter)

    repo.delete_all()

    yield repo

    repo.delete_all()
