from pynput import keyboard

from gui import draw_map


MAP_FILE_PATH = "resources/map_2_v2"


class Map:
    """The map / field of the game."""

    def __init__(self, map_file_path):
        with open(map_file_path) as map_file:
            self.map = map_file.read()


game_map = Map(MAP_FILE_PATH) # Not "map", since map is a function from the standard library

while True:
    draw_map(game_map)
    print('What do you want to do:')
    ri = input()