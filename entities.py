from random import randint

from utils import UnaliveException


D20 = 20


class Entity:

    BASE_HIT_DIE = 8 # 1d8
    BASE_AC = 10

    # TODO - More state - dead/alive, etc., spells, some stuff for testing
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
        if not self.alive:
            raise UnaliveException

        roll = randint(1, D20) + self._level
        if success := roll >= target.ac:
            damage = sum(randint(1, self.BASE_HIT_DIE)
                                 for _ in range(self._level))
            target.take_damage(damage)
        else:
            damage = 0
        return success, roll, damage

    def move(self, movement_vector):
        self.position = tuple(map(sum, zip(self.position,
                                           movement_vector)))

    def take_damage(self, damage):
        self.health -= damage


class Character(Entity):

    ICON = '░'


class Enemy(Entity):

    ICON = '¼'
