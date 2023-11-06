class Entity:
    def __init__(self, position):
        self.position = position
    
    def move(self, movement_vector):
        self.position = tuple(map(sum, zip(self.position, movement_vector)))

class Character(Entity):
    
    ICON = "C"