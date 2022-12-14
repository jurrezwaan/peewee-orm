import models
from peewee import fn
from typing import List
# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish() -> models.Dish:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """

    for dish in models.Dish.select(
            fn.MIN(models.Dish.price_in_cents)):
        lowest_price = dish.price_in_cents

    return models.Dish.get(models.Dish.price_in_cents == lowest_price)


def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    return [dish for dish in models.Dish.select().join(models.DishIngredient).join(models.Ingredient)
            if all(ingredient.is_vegetarian for ingredient in dish.ingredients)]


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """

    return (models.Restaurant
            .select(models.Restaurant,
                    models.Rating.id,
                    models.Rating.restaurant_id,
                    fn.AVG(models.Rating.rating),
                    models.Rating.comment)
            .join(models.Rating)
            .group_by(models.Rating.restaurant_id)
            .order_by(fn.AVG(models.Rating.rating).desc())
            .first())


def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """
    models.Rating.insert({models.Rating.restaurant_id: 1,
                         models.Rating.rating: 4}).execute()


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """

    return [restaurant for restaurant in
            (models.Restaurant
             .select(models.Restaurant, models.Dish)
             .join(models.Dish)
             .join(models.DishIngredient)
             .join(models.Ingredient)
             .where(models.Restaurant.closing_time >= '19:00')
             .group_by(models.Dish.name))
            if all(ingredient.is_vegan for ingredient in restaurant.dish.ingredients)
            ]


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    ingredient_data = [
        ("milk", True, False, True),
        ("macaroni", True, True, False)
    ]

    for ingredient in ingredient_data:
        models.Ingredient.get_or_create(
            name=ingredient[0],
            is_vegetarian=ingredient[1],
            is_vegan=ingredient[2],
            is_glutenfree=ingredient[3])

    ingredient_1_id = models.Ingredient.get(
        models.Ingredient.name == 'cheese').id
    ingredient_2_id = models.Ingredient.get(
        models.Ingredient.name == 'macaroni').id

    models.Dish.get_or_create(
        name='Mac n Cheese',
        served_at_id=1,
        price_in_cents=500)

    dish_id = models.Dish.get(models.Dish.name == 'Mac n Cheese').id

    models.DishIngredient.get_or_create(
        dish_id=dish_id,
        ingredient_id=ingredient_1_id)

    models.DishIngredient.get_or_create(
        dish_id=dish_id,
        ingredient_id=ingredient_2_id)

    return (models.Dish
            .get(models.Dish.name == 'Mac n Cheese'))
