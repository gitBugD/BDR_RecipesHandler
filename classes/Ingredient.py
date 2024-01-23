from .Allergen import Allergen
from .Season import Season
from .Restriction import Restriction

class Ingredient:
    name : str
    id : int
    quantity: float
    unit : str
    allergen : Allergen
    seasons = [Season]
    not_suitable_for = [Restriction]
    
    def __init__(self):
        self.name = ''
        self.id = 0
        self.allergen = Allergen()

    def __init__(self, name : str, id : int, quantity : float = 0, unit : str = '', allergen : Allergen = None):
        self.name = name
        self.id = id
        self.quantity = quantity
        self.unit = unit
        self.allergen = allergen
        self.seasons = []
        self.not_suitable_for = []

    def add_season (self, season : Season):
        self.seasons.append(season)

    def add_multiple_seasons (self, seasons: [Season]):
        for season in seasons:
            self.seasons.append(season)

    def add_negative_restriction (self, restriction : Restriction):
        self.not_suitable_for.append(restriction)

    def remove_season (self, season : Season):
        self.seasons.remove(season)

    def remove_negative_restriction (self, restriction : Restriction):
        self.not_suitable_for.remove(restriction)