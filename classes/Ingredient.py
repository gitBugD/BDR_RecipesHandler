from .Allergen import Allergen

class Ingredient:
    name : str
    id : int
    quantity: float
    unit : str
    allergen : Allergen
    
    def __init__(self, name : str, id : int, quantity : float = 0, unit : str = '', allergen : Allergen = None):
        self.name = name
        self.id = id
        self.quantity = quantity
        self.unit = unit
        self.allergen = allergen