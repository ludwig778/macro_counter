from ingredients.base import LiquidIngredient, SolidIngredient


ingredients = {
    "tomato": SolidIngredient(
        "Tomato",
        units=100,
        kcal=18,
        protein=0.9,
        carb=3.9,
        fat=0.2,
        poly_fat=0.1,
        fiber=1.2,
        sugar=2.6
    ),
    "coco_oil": LiquidIngredient(
        "Coconut Oil",
        units=100,
        kcal=863,
        fat=100,
        saturated_fat=93.8,
    ),
    "coco_milk": LiquidIngredient(
        "Coconut Milk",
        units=90,
        kcal=170,
        protein=1,
        carb=2,
        fat=17,
        saturated_fat=15,
        sugar=2
    ),
    "butter": SolidIngredient(
        "Butter",
        units=100,
        kcal=717,
        protein=0.9,
        carb=0.1,
        fat=81,
        saturated_fat=51,
        mono_fat=21,
        poly_fat=3,
        trans_fat=3.3,
        sugar=0.1
    )
}
