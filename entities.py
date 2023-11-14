from math import dist
from random import randint

from utils import OutOfRangeError, UnaliveException


D20 = 20


class Entity:

    ATTACK_RANGE = 5
    BASE_HIT_DIE = 8 # 1d8
    BASE_AC = 10

    def __init__(self, name, level, health, position, fav_position):
        self.name = name
        self._level = level
        self.health = health
        self.position = position
        self.__fav_position = fav_position
        self.ac = self.BASE_AC + level

    @property
    def alive(self):
        """Return if the entity is alive or not."""
        return self.health > 0

    def attack(self, target):
        """Attempt an attack on a target.

        Whether or not the target is hit is calculated via modified
        D&D rules. Very modified.
        """
        if not self.alive:
            raise UnaliveException

        if dist(self.position, target.position) > self.ATTACK_RANGE:
            raise OutOfRangeError

        roll = randint(1, D20) + self._level
        if success := roll >= target.ac:
            damage = sum(randint(1, self.BASE_HIT_DIE)
                                 for _ in range(self._level))
            target.take_damage(damage)
        else:
            damage = 0
        return success, roll, damage

    def move(self, movement_vector):
        """Change the position of the current entity."""
        self.position = tuple(map(sum, zip(self.position,
                                           movement_vector)))

    def take_damage(self, damage):
        """OUCH!

        Okay, hear me out, this is not a good docstring.
        Don't take this as an example of what you should be doing.
        However, I do like to make it fun for myself from time to time.
        Deal with it.
        """
        self.health -= damage


class Character(Entity):

    ICON = '░'


class Enemy(Entity):

    ICON = '¼'
