from dataclasses import asdict
from pathlib import Path

from macro_counter.settings import AppSettings


def test_settings_with_default_docker_env_variables():
    assert asdict(AppSettings.build()) == {
        "test": True,
        "debug": False,
        "config": {"path": Path(".testing/macro_counter/config.json")},
        "store": {"path": Path(".testing/macro_counter/store.json").absolute()},
        "price_enabled": False,
    }
