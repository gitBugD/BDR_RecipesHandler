class Tool:
    name : str
    id : int
    
    def __init__(self):
        self.name = ''
        self.id = 0
    
    def __init__(self, name : str, id : int):
        self.name = name
        self.id = id