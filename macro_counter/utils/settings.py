from dataclasses import asdict

from hartware_lib.adapters.filesystem import FileAdapter
from hartware_lib.serializers import serialize

from macro_counter.settings import AppSettings


def create_config_file(settings: AppSettings) -> None:
    config_file = FileAdapter(path=settings.config.path)
    config_file.directory.create()

    settings_dict = asdict(settings)

    for k in ("config", "test", "debug"):
        del settings_dict[k]

    config_file.write(serialize(settings_dict, indent=4))
