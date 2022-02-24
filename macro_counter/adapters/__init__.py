from typing import Optional, Union

from hartware_lib.adapters.file import FileAdapter
from pydantic import BaseModel

from macro_counter.adapters.mongo import MongoAdapter
from macro_counter.settings import AppSettings

AdapterInstance = Union[FileAdapter, MongoAdapter]


class Adapters(BaseModel):
    local_store: FileAdapter
    mongo: Optional[MongoAdapter]
    current: AdapterInstance

    class Config:
        arbitrary_types_allowed = True


def get_adapters(settings: AppSettings) -> Adapters:
    mongo = (
        MongoAdapter(settings.mongo_settings)
        if settings.mongo_settings.is_valid
        else None
    )
    local_store = FileAdapter(settings.local_store.path)
    local_store.create_parent_dir()

    return Adapters(
        mongo=mongo,
        local_store=local_store,
        current=mongo if mongo and mongo.connected else local_store,
    )
