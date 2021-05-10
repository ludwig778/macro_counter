from os import environ

TEST = environ.get("TEST", False)

PROMPT_BASE_NAME = environ.get("PROMPOT_BASE_NAME", "counter")

MONGO_CONFIG = {}

for key, default in (
    ("MONGODB_USERNAME", None),
    ("MONGODB_PASSWORD", None),
    ("MONGODB_HOST",     None),
    ("MONGODB_PORT",     27017)
):
    attr = environ.get(key, default)

    assert attr, f"{key} must be set"

    MONGO_CONFIG[key.replace("MONGODB_", "").lower()] = attr

MONGO_DATABASE = environ.get("MONGODB_DATABASE", "macro_counter")
