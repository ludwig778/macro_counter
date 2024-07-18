from dataclasses import asdict
from typing import Dict, List

from hartware_lib.serializers import deserialize, serialize

from macro_counter.adapters import FileAdapter
from macro_counter.exceptions import (ComponentAlreadyExist,
                                      ComponentDoesNotExist)
from macro_counter.models import Component
from macro_counter.repositories.abstract import AbstractComponentRepository


class LocalComponentRepository(AbstractComponentRepository):
    def __init__(self, store: FileAdapter):
        self.store = store

    def save(self, data: Dict) -> None:
        return self.store.write(serialize(data))

    def read(self) -> Dict:
        return deserialize(self.store.read())

    def create(self, component: Component) -> Component:
        local_data = self.read()

        if local_data.get(component.name):
            raise ComponentAlreadyExist(component.name)
        else:
            local_data[component.name] = asdict(component)

            self.save(local_data)

            return component

    def update(self, component: Component) -> Component:
        local_component = self.get(component.name)

        if asdict(local_component) != asdict(component):
            local_data = self.read()

            local_data[component.name] = asdict(component)

            self.save(local_data)

        return component

    def get(self, component_name: str) -> Component:
        local_data = self.read()

        if component_data := local_data.get(component_name):
            return Component(**component_data)
        else:
            raise ComponentDoesNotExist(component_name)

    def list(self) -> List[Component]:
        return [
            Component(**component_data)
            for component_data in self.read().values()
        ]

    def delete(self, component: Component) -> bool:
        local_data = self.read()

        if local_data.get(component.name):
            del local_data[component.name]

            self.save(local_data)

            return True
        else:
            raise ComponentDoesNotExist(component.name)

    def delete_all(self) -> bool:
        self.save({})

        return True
