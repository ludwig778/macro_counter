from typing import List

from macro_counter.adapters import FileAdapter
from macro_counter.exceptions import ComponentAlreadyExist, ComponentDoesNotExist
from macro_counter.models import Component
from macro_counter.repositories.components.abstract import AbstractComponentRepository


class LocalComponentRepository(AbstractComponentRepository):
    def __init__(self, local_store: FileAdapter):
        self.local_store = local_store

    def create(self, component: Component) -> Component:
        local_data = self.local_store.read_json()

        if local_data.get(component.name):
            raise ComponentAlreadyExist(component.name)
        else:
            local_data[component.name] = component.dict()

            self.local_store.write_json(local_data)

            return component

    def update(self, component: Component) -> Component:
        local_component = self.get(component.name)

        if local_component.dict() != component.dict():
            local_data = self.local_store.read_json()

            local_data[component.name] = component.dict()

            self.local_store.write_json(local_data)

        return component

    def get(self, component_name: str) -> Component:
        local_data = self.local_store.read_json()

        if component_data := local_data.get(component_name):
            return Component(**component_data)
        else:
            raise ComponentDoesNotExist(component_name)

    def list(self) -> List[Component]:
        return [
            Component(**component_data)
            for component_data in self.local_store.read_json().values()
        ]

    def delete(self, component: Component) -> bool:
        local_data = self.local_store.read_json()

        if local_data.get(component.name):
            del local_data[component.name]

            self.local_store.write_json(local_data)

            return True
        else:
            raise ComponentDoesNotExist(component.name)

    def delete_all(self) -> bool:
        self.local_store.write_json({})

        return True
