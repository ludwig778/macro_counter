from typing import List

from macro_counter.adapters import FileAdapter
from macro_counter.exceptions import ComponentAlreadyExist, ComponentDoesNotExist
from macro_counter.models import Component
from macro_counter.repositories.components.abstract import AbstractComponentRepository


class LocalComponentRepository(AbstractComponentRepository):
    def __init__(self, file_adapter: FileAdapter):
        self.file = file_adapter

    def create(self, component: Component) -> Component:
        local_data = self.file.load()

        if local_data.get(component.name):
            raise ComponentAlreadyExist(component.name)
        else:
            local_data[component.name] = component.dict()

            self.file.save(local_data)

            return component

    def update(self, component: Component) -> Component:
        local_component = self.get(component.name)

        if local_component.dict() != component.dict():
            local_data = self.file.load()

            local_data[component.name] = component.dict()

            self.file.save(local_data)

        return component

    def get(self, component_name: str) -> Component:
        local_data = self.file.load()

        if component_data := local_data.get(component_name):
            return Component(**component_data)
        else:
            raise ComponentDoesNotExist(component_name)

    def list(self) -> List[Component]:
        return [
            Component(**component_data) for component_data in self.file.load().values()
        ]

    def delete(self, component: Component) -> bool:
        local_data = self.file.load()

        if local_data.get(component.name):
            del local_data[component.name]

            self.file.save(local_data)

            return True
        else:
            raise ComponentDoesNotExist(component.name)

    def delete_all(self) -> bool:
        self.file.save({})

        return True
