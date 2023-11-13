from math import dist
from pynput import keyboard

import gui
import entities

from utils import CollisionError, NoOneToPlayError, VectorPosition


MAP_FILE_PATH = "resources/map_2_v2"


class _TupleIndexedMatrix(list):
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
    CHARACTER_INIT_POSITION = (18, 6)

    def __init__(self, map_file_path):
        with open(map_file_path) as map_file:
            self._blank_map = _TupleIndexedMatrix(list(row) for row in map_file.readlines())
        try:
            self.character = entities.Character('Petkan',
                                                5,
                                                100,
                                                self.CHARACTER_INIT_POSITION,
                                                '69')
        except (AttributeError, NameError, TypeError):
            raise NoOneToPlayError
        self.enemies = []
        self.enemies.append(entities.Enemy('Murshata',
                                           10,
                                           150,
                                           (15, 15),
                                           'Пират'))
        self.update()

    def __str__(self):
        return ''.join(''.join(row) for row in self._map)
    
    def __getitem__(self, index):
        return self._map[index]
    
    def update(self):
        """Reset the map to it's default state and redraw the moveable objects."""
        self._map = self._blank_map.deepcopy()
        self._map[self.character.position] = self.character.ICON
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
            self.map = Map(MAP_FILE_PATH)
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
            success, roll, damage = self.map.character.attack(target)
            self.gui.add_attack_summary(success,
                                        attacker=self.map.character.name,
                                        target=target.name,
                                        target_ac=target.ac,
                                        health_left=target.health,
                                        roll=roll,
                                        damage=damage,
                                        )
        except (AttributeError, NotImplementedError):
            self.gui.add_message(gui.NO_ATTACK_MESSAGE)

    def handle_collision(self, movement_vector):
        """Raise a CollisionError when there are colliding objects."""
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


engine = Engine(enable_pynput=True)
engine.mainloop()