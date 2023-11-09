class CollisionError(Exception):
    pass

class VectorPosition(tuple):
    def __add__(self, other):
        return VectorPosition(map(sum, zip(self, other)))