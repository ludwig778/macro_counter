from macro_counter.repository import ingredient_collection


class Ingredient:
    def __init__(self, name, kind=None, units=None, attrs=None, **kwargs):
        self.name = name

        if not kind:
            raise Exception("Kind must be set")

        self.kind = kind
        self.units = units or 1
        self.attrs = attrs or {}

    @property
    def measure(self):
        return "gr" if self.kind == "solid" else "ml"

    @classmethod
    def create(cls, name, **kwargs):
        if not (obj := cls.get(name)):
            obj = cls(name, **kwargs)

            ingredient_collection.insert_one(obj.to_dict())

        return obj

    @classmethod
    def list(cls, **kwargs):
        return [
            cls(**ingr)
            for ingr in ingredient_collection.find(kwargs)
        ]

    @classmethod
    def get(cls, name):
        ingredient = ingredient_collection.find_one({"name": name})

        if ingredient:
            return cls(**ingredient)

    def update(self, **kwargs):
        self_data = self.to_dict()
        new_data = {**self_data, **kwargs}

        if self_data != new_data:
            ingredient_collection.update_one({"name": self.name}, {"$set": new_data})

            self.__dict__.update(new_data)

    def delete(self):
        return ingredient_collection.delete_one({"name": self.name})

    def copy(self):
        return self.__class__(**self.to_dict())

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} {self.units}{self.measure}>"

    def to_dict(self):
        return {
            "name": self.name,
            "units": self.units,
            "kind": self.kind,
            "attrs": self.attrs
        }

    def multiply(self, val):
        self.units *= val

        new_attrs = {}

        for k, v in self.attrs.items():
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


class IngredientList(object):
    def __init__(self, members=None):
        self.members = members or []

    def append(self, member):
        self.members.append(member)

    def sum(self):
        attrs = {"units": 0}

        for member in self.members:
            attrs["units"] += member.units

            for k, v in member.attrs.items():
                if k not in attrs:
                    attrs[k] = 0

                attrs[k] += v

        return attrs
