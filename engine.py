import json
from math import dist
from pynput import keyboard

import gui
import entities
from utils import (CollisionError, NoOneToPlayError, OutOfRangeError,
                   UnaliveException, VectorPosition)


LEVEL_CONFIG_FILE_PATH = "resources/level_config.json"
MAP_FILE_PATH = "resources/map_2_v2"


class _TupleIndexedMatrix(list):
    """A 2-dimensional matrix which allows indexing by tuples (position).

    Example usage:
    >>> map = _TupleIndexedMatrix([[1, 2], [3, 4]])
    >>> print(map[(1, 1)])
    4
    """
    def __getitem__(self, index):
        if isinstance(index, tuple):
            return super().__getitem__(index[0])[index[1]]
        else:
            return super().__getitem__(index)

    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            self[index[0]][index[1]] = value
        else:
            self[index] = value

    def deepcopy(self):
        return _TupleIndexedMatrix(row[:] for row in self)


class Map:
    """The map / field of the game."""
    WALLS = '=|#'
    EMPTY = ' '

    def __init__(self, map_file_path, level_config_file_path):
        """Read the map and configuration from files and populate the map."""
        with open(map_file_path) as map_file:
            self._blank_map = _TupleIndexedMatrix(list(row) for row in map_file.readlines())
        with open(level_config_file_path) as level_config_file:
            level_config = json.load(level_config_file)
        # Since json doesn't support fancy objects trivially,
        # create a VectorPosition from the coordinates in the level config
        character_config = level_config['character']
        character_config['position'] = VectorPosition(character_config['position'])
        self.character = entities.Character(**character_config)
        self.enemies = []
        for enemy in level_config['enemies']:
            enemy['position'] = VectorPosition(enemy['position'])
            self.enemies.append(entities.Enemy(**enemy))
        self.update()

    def __str__(self):
        return ''.join(''.join(row) for row in self._map)

    def __getitem__(self, index):
        return self._map[index]

    def update(self):
        """Reset the map to it's default state and redraw the moveable objects."""
        self._map = self._blank_map.deepcopy()
        self._map[self.character.position] = self.character.ICON
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        for enemy in self.enemies:
            self._map[enemy.position] = enemy.ICON


class Engine:
    """Engine that runs the game and parses all the inputs."""

    MOVEMENT_VECTORS = {'w': VectorPosition((-1, 0)),
                        's': VectorPosition((1, 0)),
                        'a': VectorPosition((0, -1)),
                        'd': VectorPosition((0, 1))}

    def __init__(self, enable_pynput):
        self.gui = gui.Gui()
        try:
            self.map = Map(MAP_FILE_PATH, LEVEL_CONFIG_FILE_PATH)
        except NoOneToPlayError:
            self.gui.exit(gui.NO_ONE_TO_PLAY_MESSAGE)
        self._enable_pynput = enable_pynput
        self.ACTION_CALLBACKS = {'x': self.handle_attack,
                                 'c': self.handle_spellcasting,
                                 'q': self.handle_exit}

    def mainloop(self):
        while True:
            self.gui.draw_screen(self.map)
            self.parse_input()
            self.map.update()

    def handle_attack(self):
        """Trigger an attack of the player object."""
        target = min(self.map.enemies,
                     key = lambda enemy: dist(self.map.character.position,
                                              enemy.position))
        # Handle missing implementation
        try:
            self.perform_attack(self.map.character, target)
            # Target retaliates
            if target.alive:
                self.perform_attack(target, self.map.character)
        except (AttributeError, NotImplementedError):
            self.gui.add_message(gui.NO_ATTACK_MESSAGE)
        except UnaliveException:
            self.gui.add_message(gui.NO_LIFE_MESSAGE)
        except OutOfRangeError:
            self.gui.add_message(gui.NO_ENEMIES_IN_RANGE)

    def handle_collision(self, movement_vector):
        """Raise a CollisionError when there are colliding objects."""
        if not self.map.character.alive:
            return # Yes, skip collision if the character is a ghost
        new_position = movement_vector + self.map.character.position
        if self.map[new_position] in self.map.WALLS:
            raise CollisionError(gui.WALL_COLLISION_MESSAGE)
        if new_position in [enemy.position for enemy in self.map.enemies]:
            raise CollisionError(gui.ENEMY_COLLISION_MESSAGE)

    def handle_exit(self):
        self.gui.exit()

    def handle_movement(self, key_pressed):
        """Trigger a move of the player object depending on the chosen direction."""
        try:
            self.handle_collision(self.MOVEMENT_VECTORS[key_pressed])
        except CollisionError as err:
            self.gui.add_message(str(err))
        else:
            # Handle missing implementation
            try:
                self.map.character.move(self.MOVEMENT_VECTORS[key_pressed])
            except (AttributeError, NotImplementedError):
                self.gui.add_message(gui.NO_MOVEMENT_MESSAGE)

    def handle_spellcasting(self):
        """Trigger a move of the player object depending on the chosen direction."""
        # Handle missing implementation
        try:
            self.map.character.cast_spell()
        except (AttributeError, NotImplementedError):
            self.gui.add_message(gui.NO_SPELLCASTING_MESSAGE)

    def parse_input(self):
        """Parse the keyboard input with either pynput (dynamic) or from standard input."""
        if self._enable_pynput:
            key_pressed = self._parse_pynput()
        else:
            key_pressed = self._parse_normal_input()
        if key_pressed in self.MOVEMENT_VECTORS:
            self.handle_movement(key_pressed)
        # Why check - because we don't want to crash when pressing a key
        # for which an action is not defined yet. It's too much hassle.
        if key_pressed in self.ACTION_CALLBACKS:
            self.ACTION_CALLBACKS[key_pressed]()

    def _parse_normal_input(self):
        return input()

    def _parse_pynput(self):
        key_pressed = None
        def on_release(key):
            nonlocal key_pressed
            key_pressed = key
            return False

        with keyboard.Listener(on_release=on_release) as listener:
            listener.join()
        return key_pressed.char

    def perform_attack(self, attacker, target):
        """Perform the attack action and log the attack to the output buffer."""
        success, roll, damage = attacker.attack(target)
        self.gui.add_attack_summary(success,
                                    attacker=attacker.name,
                                    target=target.name,
                                    target_ac=target.ac,
                                    health_left=target.health,
                                    roll=roll,
                                    damage=damage)


engine = Engine(enable_pynput=True)
engine.mainloop()