from abc import ABC, abstractmethod
from typing import List

from macro_counter.models import Component


class AbstractComponentRepository(ABC):
    @abstractmethod
    def create(self, component: Component) -> Component:
        pass

    @abstractmethod
    def update(self, component: Component) -> Component:
        pass

    @abstractmethod
    def get(self, component_name: str) -> Component:
        pass

    @abstractmethod
    def list(self) -> List[Component]:
        pass

    @abstractmethod
    def delete(self, component: Component) -> bool:
        pass

    @abstractmethod
    def delete_all(self) -> bool:
        pass
