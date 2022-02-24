from hartware_lib.adapters.file import FileAdapter

from macro_counter.settings import AppSettings
from macro_counter.utils.json import PathEncoder


def create_config_file(settings: AppSettings) -> None:
    config_file = FileAdapter(file_path=settings.config.path)
    config_file.create_parent_dir()

    if not config_file.exists():
        print(f"Empty setting file created: {settings.config.path}")

        config_file.create_parent_dir()
        config_file.write_json(
            settings.dict(exclude={"config", "test", "debug"}), cls=PathEncoder
        )
