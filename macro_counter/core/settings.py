from os import environ
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from macro_counter.adapters.file import FileAdapter

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "macro_counter" / "config.json"
DEFAULT_STORE_PATH = Path.home() / ".config" / "macro_counter" / "store.json"


class MongoSettings(BaseModel):
    username: Optional[str]
    password: Optional[str]
    database: Optional[str]
    host: Optional[str]
    port: Optional[int] = 27017
    srv_mode: Optional[bool] = False
    timeout_ms: Optional[int] = 2000

    @property
    def is_valid(self):
        return all([self.username, self.password, self.database, self.host])


class EnvSettings(BaseModel):
    config_path: Optional[str] = environ.get("MACRO_COUNTER_CONFIG_PATH")
    local_store_path: Optional[str] = environ.get("MACRO_COUNTER_LOCAL_STORE_PATH")

    username: Optional[str] = environ.get("MACRO_COUNTER_MONGODB_USERNAME")
    password: Optional[str] = environ.get("MACRO_COUNTER_MONGODB_PASSWORD")
    database: Optional[str] = environ.get("MACRO_COUNTER_MONGODB_DATABASE")
    host: Optional[str] = environ.get("MACRO_COUNTER_MONGODB_HOST")
    port: Optional[str] = environ.get("MACRO_COUNTER_MONGODB_PORT")
    srv_mode: Optional[str] = environ.get("MACRO_COUNTER_MONGODB_SRV_MODE")
    timeout_ms: Optional[str] = environ.get("MACRO_COUNTER_MONGODB_TIMEOUT_MS")


class FileSettings(BaseModel):
    mongo_settings: MongoSettings = MongoSettings()

    local_store_path: Optional[str]


class AppSettings(BaseModel):
    env_settings: EnvSettings
    file_settings: FileSettings

    config_path: Optional[Path] = None
    mongo_settings: Optional[MongoSettings] = None
    local_store_path: Path = DEFAULT_STORE_PATH


def get_settings():
    """
    Build a setting object containing both file configuration and env variables
    """

    env_settings = EnvSettings()

    if (
        env_settings.config_path
        and (config_path := Path(env_settings.config_path)).exists()
    ):
        config_file = FileAdapter(config_path)
    else:
        config_path = DEFAULT_CONFIG_PATH

        config_file = FileAdapter(config_path)

        if not config_path.exists():
            print(f"Empty setting file created: {config_path}")

            config_file.create(FileSettings().dict())

    file_settings = FileSettings(**config_file.load())

    app_settings = AppSettings(
        env_settings=env_settings,
        file_settings=file_settings,
        config_path=str(config_file.path),
    )

    if file_settings.local_store_path:
        app_settings.local_store_path = Path(file_settings.local_store_path)

    app_settings.mongo_settings = MongoSettings(
        **{
            **file_settings.mongo_settings.dict(exclude_none=True),
            **env_settings.dict(exclude_none=True),
        }
    )

    return app_settings
