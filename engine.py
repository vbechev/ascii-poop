from pynput import keyboard

import gui
import entities

from utils import VectorPosition


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
        self.character = entities.Character(self.CHARACTER_INIT_POSITION)
        self.update()

    def __str__(self):
        return ''.join(''.join(row) for row in self._map)
    
    def __getitem__(self, index):
        return self._map[index]
    
    def update(self):
        self._map = self._blank_map.deepcopy()
        self._map[self.character.position] = self.character.ICON


class Engine:
    """Engine that runs the game and parses all the inputs."""

    MOVEMENT_VECTORS = {'w': VectorPosition((-1, 0)),
                        's': VectorPosition((1, 0)),
                        'a': VectorPosition((0, -1)),
                        'd': VectorPosition((0, 1))}
    
    def __init__(self, enable_pynput):
        self.map = Map(MAP_FILE_PATH)
        self.gui = gui.Gui()
        self._enable_pynput = enable_pynput

    def mainloop(self):
        while True:
            self.gui.draw_screen(self.map)
            self.parse_input()
            self.map.update()

    def handle_collision(self, movement_vector):
        if self.map[movement_vector + self.map.character.position] in self.map.WALLS:
            raise IndexError

    def parse_input(self):
        if self._enable_pynput:
            key_pressed = self._parse_pynput()
        else:
            key_pressed = self._parse_normal_input()
        if key_pressed == 'q':
            self.gui.exit()
        if key_pressed in self.MOVEMENT_VECTORS:
            try:
                self.handle_collision(self.MOVEMENT_VECTORS[key_pressed])
            except IndexError:
                self.gui.message(gui.COLLISION_MESSAGE)
            else:
                self.map.character.move(self.MOVEMENT_VECTORS[key_pressed])

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