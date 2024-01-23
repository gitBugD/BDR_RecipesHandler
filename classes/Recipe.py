from .Creator import Creator
from .Step import Step

class Recipe:
    name : str
    id : int
    description : str
    nbPeople : int
    difficulty : int
    cost : int
    creator : Creator
    steps = [Step]

    def __init__(self, name : str, id : int, description : str, nbPeople : int = 0, difficulty : int = 0, cost : int = 0, creator : Creator = None):
        self.name = name
        self.id = id
        self.description = description
        self.nbPeople = nbPeople
        self.difficulty = difficulty
        self.cost = cost
        self.creator = creator
        self.steps = []

    def add_step (self, step : Step):
        self.steps.append(step)

    def add_multiple_steps(self, steps : []):
        for step in steps:
            self.steps.append(step)

    def remove_step (self, step : Step):
        self.steps.remove(step)