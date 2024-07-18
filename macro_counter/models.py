from dataclasses import dataclass, field


@dataclass
class Field:
    label: str
    fullname: str
    shortname: str = ""
    macro: bool = False
    show_percents: bool = False

    @property
    def name(self):
        return self.shortname or self.fullname


unit_field = Field(label="units", fullname="Units")

protein_field = Field(
    label="protein",
    fullname="Protein",
    shortname="Prot",
    macro=True,
    show_percents=True,
)
carb_field = Field(label="carb", fullname="Carb", macro=True, show_percents=True)
fat_field = Field(label="fat", fullname="Fat", macro=True, show_percents=True)
price_field = Field(label="price", fullname="Price", macro=False, show_percents=True)

macro_fields = [protein_field, carb_field, fat_field]

attrs_fields = [
    Field(label="kcal", fullname="Calories", shortname="Cal"),
    protein_field,
    carb_field,
    Field(
        label="fiber",
        fullname="Fiber",
    ),
    Field(label="sugar", fullname="Sugar", show_percents=True),
    fat_field,
    Field(
        label="saturated_fat",
        fullname="Saturated fat",
        shortname="Sat",
        show_percents=True,
    ),
    Field(
        label="mono_fat",
        fullname="Mono insaturated fat",
        shortname="Mono",
        show_percents=True,
    ),
    Field(
        label="poly_fat",
        fullname="Poly insaturated fat",
        shortname="Poly",
        show_percents=True,
    ),
    Field(
        label="trans_fat", fullname="Trans fat", shortname="Trans", show_percents=True
    ),
]


class ComponentKind:
    SOLID = "solid"
    LIQUID = "liquid"


@dataclass
class Component:
    name: str
    kind: str

    units: float = 1.0
    attrs: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.kind not in ("solid", "liquid"):
            raise ValueError('Component kind must be either "solid" or "liquid"')

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
