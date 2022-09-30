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

    query = (models.Dish
             .select(models.Dish.id,
                     models.Dish.name, models.Dish.served_at,
                     fn.MIN(models.Dish.price_in_cents)))
    return query


...


def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    ...

    dish_list = []
    query = models.Dish.select()
    for dish in query:
        dish_list.append(dish)

    query = (models.DishIngredient.select()
             .join(models.Dish)
             .switch(models.DishIngredient)
             .join(models.Ingredient)
             .where(models.Ingredient.is_vegetarian == 0))

    for dishingredient in query:
        if dishingredient.dish in dish_list:
            dish_list.remove(dishingredient.dish)
    return dish_list


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """

    query = (models.Rating
             .select(models.Rating.id,
                     models.Rating.restaurant_id,
                     fn.AVG(models.Rating.rating),
                     models.Rating.comment)
             .group_by(models.Rating.restaurant_id)
             .order_by(fn.AVG(models.Rating.rating).desc()).first())

    return models.Restaurant.select().where(
        query.restaurant_id == models.Restaurant.id)

    ...


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

    restaurants_open = (models.Restaurant
                        .select()
                        .where(models.Restaurant.closing_time > '19:00')
                        .dicts())
    for restaurant in restaurants_open:
        print(restaurant)

    not_vegan_dish = (models.DishIngredient
                      .select(models.DishIngredient,
                              models.Ingredient, models.Dish)
                      .join(models.Ingredient,
                            on=(models.DishIngredient.
                                ingredient_id == models.Ingredient.id))
                      .switch()
                      .join(models.Dish, on=(models.DishIngredient.
                                             dish_id == models.Dish.id))
                      .where(models.Ingredient.is_vegan == 0)
                      .group_by(models.DishIngredient.dish_id)
                      .dicts())
    all_dishes = models.Dish.select().dicts()

    vegan_dish = all_dishes - not_vegan_dish
    print(vegan_dish)

    ...


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    ...
