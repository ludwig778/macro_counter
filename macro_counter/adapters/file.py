from json import dump, load
from pathlib import Path
from typing import Optional


class FileAdapter:
    def __init__(self, path: Path):
        self.path = path

    def create(self, data: Optional[dict] = None):
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True)

        if not self.path.exists():
            self.save(data or {})

            return True

        return False

    def delete(self):
        self.path.unlink()

    def load(self) -> dict:
        with open(self.path) as fd:
            return load(fd)

    def save(self, data: dict) -> None:
        with open(self.path, "w") as fd:
            dump(data, fd, indent=2)
