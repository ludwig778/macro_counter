from pathlib import Path

from hartware_lib.adapters.file import FileAdapter
from hartware_lib.pydantic.field_types import BooleanFromString
from pydantic import BaseSettings, Field

from macro_counter.utils.pydantic import use_env_variables_over_config_file

BASE_PATH: Path = Path.home() / ".config" / "macro_counter"
DEFAULT_CONFIG_PATH: Path = BASE_PATH / "config.json"
DEFAULT_STORE_PATH: Path = BASE_PATH / "store.json"


class MongoSettings(BaseSettings):
    username: str = ""
    password: str = ""
    database: str = ""
    host: str = ""
    port: int = 27017
    srv_mode: BooleanFromString = Field(default=False)
    timeout_ms: int = 2000

    @property
    def is_valid(self):
        return all([self.username, self.password, self.database, self.host])

    class Config:
        case_sensitive = False
        env_prefix = "MACRO_COUNTER_MONGODB_"

        customise_sources = use_env_variables_over_config_file


class LocalConfigSettings(BaseSettings):
    path: Path = DEFAULT_CONFIG_PATH

    class Config:
        case_sensitive = False
        env_prefix = "MACRO_COUNTER_CONFIG_"


class LocalStoreSettings(BaseSettings):
    path: Path = DEFAULT_STORE_PATH

    class Config:
        case_sensitive = False
        env_prefix = "MACRO_COUNTER_LOCAL_STORE_"
        customise_sources = use_env_variables_over_config_file


class AppSettings(BaseSettings):
    test: BooleanFromString = Field(default=False)
    debug: BooleanFromString = Field(default=False)

    config: LocalConfigSettings = Field(default_factory=LocalConfigSettings)
    mongo_settings: MongoSettings = Field(default_factory=MongoSettings)
    local_store: LocalStoreSettings = Field(default_factory=LocalStoreSettings)

    class Config:
        case_sensitive = False
        env_prefix = "MACRO_COUNTER_"


def get_settings():
    """
    Build a setting object containing both file configuration and env variables
    """

    local_config_settings = LocalConfigSettings()
    local_config_file = FileAdapter(file_path=local_config_settings.path)

    if local_config_file.exists():
        return AppSettings(**local_config_file.read_json())

    return AppSettings()
