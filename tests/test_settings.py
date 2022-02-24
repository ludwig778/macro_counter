from pathlib import Path

from hartware_lib.adapters.file import FileAdapter

from macro_counter.settings import get_settings
from macro_counter.utils.settings import create_config_file


def test_settings_with_default_docker_env_variables():
    assert get_settings().dict() == {
        "test": True,
        "debug": False,
        "config": {"path": Path(".testing/macro_counter/config.json")},
        "mongo_settings": {
            "database": "macro_counter",
            "host": "mongodb",
            "password": "password123",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "user",
        },
        "local_store": {"path": Path(".testing/macro_counter/store.json")},
    }


def test_settings_with_only_env_variables(monkeypatch):
    monkeypatch.setenv("MACRO_COUNTER_TEST", "true")
    monkeypatch.setenv("MACRO_COUNTER_DEBUG", "false")
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_USERNAME", "username")
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_PASSWORD", "password")
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_HOST", "host")
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_DATABASE", "database")

    assert get_settings().dict() == {
        "test": True,
        "debug": False,
        "config": {"path": Path(".testing/macro_counter/config.json")},
        "mongo_settings": {
            "database": "database",
            "host": "host",
            "password": "password",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "username",
        },
        "local_store": {"path": Path(".testing/macro_counter/store.json")},
    }


def test_settings_create_config_file(monkeypatch):
    monkeypatch.setenv("MACRO_COUNTER_TEST", "true")
    monkeypatch.setenv("MACRO_COUNTER_DEBUG", "false")
    monkeypatch.setenv(
        "MACRO_COUNTER_CONFIG_PATH", ".testing/macro_counter/config.json"
    )
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_USERNAME", "username")
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_PASSWORD", "password")
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_HOST", "host")
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_DATABASE", "database")
    monkeypatch.setenv(
        "MACRO_COUNTER_LOCAL_STORE_PATH", ".testing/macro_counter/store.json"
    )

    settings = get_settings()

    create_config_file(settings)

    config_file = FileAdapter(file_path=Path(".testing/macro_counter/config.json"))

    assert config_file.read_json() == {
        "local_store": {"path": ".testing/macro_counter/store.json"},
        "mongo_settings": {
            "database": "database",
            "host": "host",
            "password": "password",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "username",
        },
    }


def test_settings_with_mixed_source(monkeypatch):
    config_file = FileAdapter(file_path=Path(".testing/macro_counter/config.json"))
    config_file.create_parent_dir()

    config_file.write_json(
        {
            "local_store": {"path": ".testing/macro_counter/store.json"},
            "mongo_settings": {
                "database": "macro_counter",
                "host": "mongodb",
                "password": "password123",
                "port": 27017,
                "srv_mode": False,
                "timeout_ms": 2000,
                "username": "user",
            },
        }
    )

    monkeypatch.setenv("MACRO_COUNTER_TEST", "false")
    monkeypatch.setenv("MACRO_COUNTER_DEBUG", "true")
    monkeypatch.setenv(
        "MACRO_COUNTER_CONFIG_PATH", ".testing/macro_counter/config.json"
    )
    monkeypatch.setenv("MACRO_COUNTER_MONGODB_USERNAME", "overrided")
    monkeypatch.setenv(
        "MACRO_COUNTER_LOCAL_STORE_PATH", ".testing/macro_counter/store2.json"
    )

    assert get_settings().dict() == {
        "test": False,
        "debug": True,
        "config": {"path": Path(".testing/macro_counter/config.json")},
        "mongo_settings": {
            "database": "macro_counter",
            "host": "mongodb",
            "password": "password123",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "overrided",
        },
        "local_store": {"path": Path(".testing/macro_counter/store2.json")},
    }
