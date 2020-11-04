

class BaseIngredient(object):
    def __init__(self, name, units=None, **kwargs):
        self.name = name
        self.units = units or 1
        self.attrs = {
            k: v
            for k, v in kwargs.items()
            if type(v) in (int, float)
        }

    @classmethod
    def create(cls, name, **kwargs):
        return cls(name, **kwargs)

    def copy(self):
        return self.create(
            self.name,
            units=self.units,
            **self.attrs
        )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} {self.units}{self.MEASURE}>"

    def export(self):
        return {
            "type": self.TYPE,
            "attrs": self.attrs
        }

    def multiply(self, val):
        self.units *= val

        new_attrs = {}

        for k, v in self.attrs.items():
            new_attrs[k] = v * val

        self.attrs = new_attrs

    def __mul__(self, val):
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


class LiquidIngredient(BaseIngredient):
    TYPE = "liquid"
    MEASURE = "ml"

    def __init__(self, *args, milliliters=None, **kwargs):
        kwargs.setdefault("units", milliliters)
        super().__init__(*args, **kwargs)


class SolidIngredient(BaseIngredient):
    TYPE = "solid"
    MEASURE = "gr"

    def __init__(self, *args, grams=None, **kwargs):
        kwargs.setdefault("units", grams)
        super().__init__(*args, **kwargs)
