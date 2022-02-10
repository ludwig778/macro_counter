from typing import Union

from pydantic import BaseModel

from macro_counter.adapters.file import FileAdapter
from macro_counter.adapters.mongo import MongoAdapter
from macro_counter.core.settings import get_settings

AdapterInstance = Union[FileAdapter, MongoAdapter]


class Adapters(BaseModel):
    file: FileAdapter
    mongo: MongoAdapter
    current: AdapterInstance

    class Config:
        arbitrary_types_allowed = True


def get_adapters() -> Adapters:
    settings = get_settings()

    mongo = MongoAdapter(settings.mongo_settings)
    file = FileAdapter(settings.local_store_path)
    file.create()

    return Adapters(mongo=mongo, file=file, current=mongo if mongo.connected else file)
