class CollisionError(Exception):
    pass


class NoOneToPlayError(Exception):
    pass


# Why is the following an "Exception" while the rest are "Error"-s?
# The mysteries of life...
class UnaliveException(Exception):
    pass


class VectorPosition(tuple):
    def __add__(self, other):
        return VectorPosition(map(sum, zip(self, other)))