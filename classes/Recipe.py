from .Creator import Creator

class Recipe:
    name : str
    id : int
    description : str
    nbPeople : int
    difficulty : int
    cost : int
    creator : Creator

    def __init__(self, name : str, id : int, description : str, nbPeople : int = 0, difficulty : int = 0, cost : int = 0, creator : Creator = None):
        self.name = name
        self.id = id
        self.description = description
        self.nbPeople = nbPeople
        self.difficulty = difficulty
        self.cost = cost
        self.creator = creator