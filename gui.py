import os
import sys


COLLISION_MESSAGE = "Oh no, you can't move through walls, unless you're a ghost."
EXIT_MESSAGE = "Bye bye, hope you had a nice time in the sex dungeon!"
MENU_TEXT = """Controls:
'w' - move up
's' - move down
'a' - move left
'd' - move right
'x' - attack
'c' - cast spell

What do you want to do:
"""


class Gui:
    def __init__(self):
        self._message = ""

    def draw_screen(self, game_map):
        self.clear_screen()
        print(game_map)
        if self._message:
            print(self._message, end="\n\n")
            self._message = ""
        print(MENU_TEXT)

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def message(self, message):
        self._message = message
    
    def exit(self):
        print(EXIT_MESSAGE)
        sys.exit(0)