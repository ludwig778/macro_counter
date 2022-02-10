from typing import Optional

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import validator


class ComponentKind:
    SOLID = "solid"
    LIQUID = "liquid"


class Component(BaseModel):
    name: str
    kind: str

    units: float = 1.0
    attrs: dict = PydanticField(default_factory=dict)

    @validator("kind")
    def validate_kind(cls, value):
        if value not in ("solid", "liquid"):
            raise ValueError('Component kind must be either "solid" or "liquid"')
        return value

    class Config:
        extra = "ignore"

    def copy(self):
        return Component(
            name=self.name, kind=self.kind, units=self.units, attrs=self.attrs
        )

    def multiply(self, val):
        self.units *= val

        new_attrs = {}

        for k, v in self.attrs.items():
            if v:
                new_attrs[k] = v * val

        self.attrs = new_attrs

    def __add__(self, other):
        obj = self.copy()

        obj.units += other.units

        for k, v in other.attrs.items():
            if k not in obj.attrs:
                obj.attrs[k] = 0

            obj.attrs[k] += v

        return obj

    def __mod__(self, val):
        obj = self.copy()

        obj.multiply(1 / obj.units)
        obj.multiply(val)

        return obj

    def __mul__(self, val):
        obj = self.copy()
        obj.multiply(val)

        return obj

    def __truediv__(self, val):
        obj = self.copy()
        obj.multiply(1 / val)

        return obj


class Field(BaseModel):
    label: str
    fullname: str
    shortname: Optional[str]
    macro: bool = False
    show_percents: bool = False

    @property
    def name(self):
        return self.shortname or self.fullname


"""
class Component:
    def __init__(self, name, kind=None, units=None, attrs=None, components=None, **kwargs):
        self.name = name

        if not kind:
            raise Exception("Kind must be set")

        self.kind = kind
        self.units = units or 1
        self.attrs = attrs or {}

        self.components = components or {}

    @classmethod
    def create(cls, name, **kwargs):
        if not (obj := cls.get(name)):
            obj = cls(name, **kwargs)

            component_collection.insert_one(obj.to_dict())

        return obj

    @property
    def measure(self):
        return "gr" if self.kind == "solid" else "ml"

    @classmethod
    def list(cls, **kwargs):
        return [
            cls(**ingr)
            for ingr in component_collection.find(kwargs)
        ]

    @classmethod
    def get(cls, name):
        component = component_collection.find_one({"name": name})

        if component:
            return cls(**component)

    def update(self, **kwargs):
        self_data = self.to_dict()
        new_data = {**self_data, **kwargs}

        if self_data != new_data:
            component_collection.update_one({"name": self.name}, {"$set": new_data})

            self.__dict__.update(new_data)

    def delete(self):
        return component_collection.delete_one({"name": self.name})

    def copy(self):
        return self.__class__(**self.to_dict())

    def to_dict(self):
        return {
            "name": self.name,
            "units": self.units,
            "kind": self.kind,
            "attrs": self.attrs,
            "components": self.components
        }

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} {self.units}{self.measure}>"

    def multiply(self, val):
        self.units *= val

        new_attrs = {}

        for k, v in self.attrs.items():
            if v:
                new_attrs[k] = v * val

        self.attrs = new_attrs

    def __mod__(self, val):
        obj = self.copy()

        obj.multiply(1 / obj.units)
        obj.multiply(val)

        return obj

    def __mul__(self, val, normalize=False):
        obj = self.copy()
        obj.multiply(val)

        return obj


class ComponentList(object):
    def __init__(self, members=None):
        self.members = members or []

    def append(self, member):
        self.members.append(member)

    @property
    def details(self):
        summary = defaultdict(float)

        for member in self.members:
            summary[member.name] += member.units

        return dict(summary)

    def sum(self):
        attrs = defaultdict(float)

        for member in self.members:
            attrs["units"] += member.units

            for k, v in member.attrs.items():
                if k not in attrs:
                    attrs[k] = 0

                attrs[k] += v

        return dict(attrs)
"""
