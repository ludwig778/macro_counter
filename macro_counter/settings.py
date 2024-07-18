from dataclasses import dataclass
from pathlib import Path

from hartware_lib.adapters.filesystem import FileAdapter
from hartware_lib.settings import load_settings, load_settings_from_file

BASE_PATH: Path = Path.home() / ".config" / "macro_counter"
DEFAULT_CONFIG_PATH: Path = BASE_PATH / "config.yaml"
DEFAULT_STORE_PATH: Path = BASE_PATH / "store.json"


@dataclass
class ConfigSettings:
    path: Path = DEFAULT_CONFIG_PATH


@dataclass
class StoreSettings:
    path: Path = DEFAULT_STORE_PATH


@dataclass
class AppSettings:
    _prefix = "MACRO_COUNTER"

    config: ConfigSettings
    store: StoreSettings

    test: bool = False
    debug: bool = False

    price_enabled: bool = False

    @classmethod
    def build(cls):
        local_config_settings = load_settings(ConfigSettings, set_prefix="MACRO_COUNTER_CONFIG")
        local_config_file = FileAdapter(path=local_config_settings.path)

        if local_config_file.exists:
            return load_settings_from_file(cls, local_config_settings.path)

        return load_settings(cls)
