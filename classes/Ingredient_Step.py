from .Ingredient import Ingredient
from .Unit import Unit

class Ingredient_Step:
    ingredient : Ingredient
    id_recipe : int
    nb_step : int
    quantity : float
    unit : Unit

    def __init__(self):
        self.ingredient = Ingredient()
        self.id_recipe = 0
        self.nb_step = 0
        self.quantity = 0
        self.unit = Unit()

    def __init__(self, ingredient : Ingredient, id_recipe : int, nb_step : int, quantity : float, unit : Unit):
        self.ingredient = ingredient
        self.id_recipe = id_recipe
        self.nb_step = nb_step
        self.quantity = quantity
        self.unit = unit