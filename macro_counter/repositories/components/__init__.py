from typing import Type, Union

from macro_counter.adapters import AdapterInstance, MongoAdapter
from macro_counter.repositories.components.local import LocalComponentRepository
from macro_counter.repositories.components.mongo import MongoComponentRepository

ComponentRepository = Union[
    Type[LocalComponentRepository],
    Type[MongoComponentRepository],
]


def component_repository_factory(adapter: AdapterInstance) -> ComponentRepository:
    if isinstance(adapter, MongoAdapter):
        return MongoComponentRepository
    else:
        return LocalComponentRepository
