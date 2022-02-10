from macro_counter.models import Field

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
