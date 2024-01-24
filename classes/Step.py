from .Tool import Tool
from datetime import time
import pandas as pd
import math

class Step:
    nb : int
    instructions : str
    prep_time : int
    cooking_time : int
    
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
