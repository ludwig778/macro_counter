from typing import List

from macro_counter.adapters import MongoAdapter
from macro_counter.exceptions import ComponentAlreadyExist, ComponentDoesNotExist
from macro_counter.models import Component
from macro_counter.repositories.components.abstract import AbstractComponentRepository


class MongoComponentRepository(AbstractComponentRepository):
    def __init__(self, mongo_adapter: MongoAdapter, collection_name="components"):
        self.mongo_collection = mongo_adapter.get_collection(collection_name)

    def create(self, component: Component) -> Component:
        if self.mongo_collection.find_one({"name": component.name}):
            raise ComponentAlreadyExist(component.name)
        else:
            self.mongo_collection.insert_one(component.dict())

            return component

    def update(self, component: Component) -> Component:
        mongo_component = self.get(component.name)

        if mongo_component.dict() != component.dict():
            self.mongo_collection.update_one(
                {"name": component.name}, {"$set": component.dict()}
            )

        return component

    def get(self, component_name: str) -> Component:
        if component_data := self.mongo_collection.find_one({"name": component_name}):
            return Component(**component_data)
        else:
            raise ComponentDoesNotExist(component_name)

    def list(self) -> List[Component]:
        return [
            Component(**component_data)
            for component_data in self.mongo_collection.find()
        ]

    def delete(self, component: Component) -> bool:
        if self.mongo_collection.find_one({"name": component.name}):
            self.mongo_collection.delete_one({"name": component.name})

            return True
        else:
            raise ComponentDoesNotExist(component.name)

    def delete_all(self) -> bool:
        for component in self.list():
            self.delete(component)

        return True
