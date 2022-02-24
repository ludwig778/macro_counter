from typing import Union

from macro_counter.adapters import AdapterInstance, MongoAdapter
from macro_counter.repositories.components.local import LocalComponentRepository
from macro_counter.repositories.components.mongo import MongoComponentRepository

ComponentRepository = Union[
    LocalComponentRepository,
    MongoComponentRepository,
]


def component_repository_factory(adapter: AdapterInstance) -> ComponentRepository:
    if isinstance(adapter, MongoAdapter):
        return MongoComponentRepository(adapter)
    else:
        return LocalComponentRepository(adapter)
