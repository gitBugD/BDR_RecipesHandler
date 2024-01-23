from .Tool import Tool
from .Ingredient_Step import Ingredient_Step
from datetime import time
import pandas as pd
import math

class Step:
    nb : int
    instructions : str
    prep_time : int
    cooking_time : int
    tools = [Tool]
    ingredients_step = [Ingredient_Step]
    
    def __init__(self):
        pass

    def __init__(self, nb : int, instructions : str, prep_time : int, cooking_time : int = 0):
        self.nb = nb
        self.instructions = instructions
        pt_hours, pt_minutes = divmod(prep_time, 60)
        self.prep_time = time(pt_hours, pt_minutes)
        ct_hours, ct_minutes = divmod(cooking_time, 60)
        if math.isnan(ct_hours) : ct_hours = 0
        if math.isnan(ct_minutes) : ct_minutes = 0
        self.cooking_time = time(int(ct_hours), int(ct_minutes))
        self.tools = []
        self.ingredients_step = []

    def add_tool (self, tool : Tool):
            self.tools.append(tool)

    def add_multiple_tools(self, tools : [Tool]):
        for tool in tools:
            self.tools.append(tool)

    def add_ingredient_step (self, ingredient : Ingredient_Step):
        self.ingredients_step.append(ingredient)

    def add_multiple_ingredients_step(self, ingredients : Ingredient_Step):
        for ingredient in ingredients:
            self.ingredients_step.append(ingredient)

    def remove_tool (self, tool : Tool):
        self.tools.remove(tool)
