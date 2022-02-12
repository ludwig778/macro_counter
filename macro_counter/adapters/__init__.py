from typing import Optional, Union

from pydantic import BaseModel

from macro_counter.adapters.file import FileAdapter
from macro_counter.adapters.mongo import MongoAdapter
from macro_counter.core.settings import create_config_file_if_missing, get_settings

AdapterInstance = Union[FileAdapter, MongoAdapter]


class Adapters(BaseModel):
    file: FileAdapter
    mongo: Optional[MongoAdapter]
    current: AdapterInstance

    class Config:
        arbitrary_types_allowed = True


def get_adapters() -> Adapters:
    settings = get_settings()

    if settings.config_path:
        create_config_file_if_missing(settings)

    mongo = (
        MongoAdapter(settings.mongo_settings)
        if settings.mongo_settings.is_valid
        else None
    )
    file = FileAdapter(settings.local_store_path)
    file.create()

    return Adapters(
        mongo=mongo, file=file, current=mongo if mongo and mongo.connected else file
    )
