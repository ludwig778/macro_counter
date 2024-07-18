from __future__ import annotations

from dataclasses import dataclass

from hartware_lib.adapters.filesystem import FileAdapter

from macro_counter.settings import AppSettings


@dataclass
class Adapters:
    store_file: FileAdapter

    @classmethod
    def build(cls, settings: AppSettings) -> Adapters:
        store_file = FileAdapter(settings.store.path)
        store_file.directory.create()

        return Adapters(store_file=store_file)
