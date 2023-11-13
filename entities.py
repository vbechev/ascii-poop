from random import randint


D20 = 20


class Entity:

    BASE_HIT_DIE = 8 # 1d8
    BASE_AC = 10

    # TODO - More state - dead/alive, etc., spells, some stuff for testing
    def __init__(self, name, level, health,
                 position, fav_position):
        self.name = name
        self._level = level
        self.health = health
        self.position = position
        self.__fav_position = fav_position
        self.ac = self.BASE_AC + level

    def attack(self, target):
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

c = Character('Gosho', 5, 100, (10, 10), 'Лешояд')
e = Enemy('Murshata', 10, 200, (10, 9), 'Не е лешояд')