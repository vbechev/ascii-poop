import os
import sys


# Attack messaging can be better done in another way, but this will have to do
ATTACK_COMMON = "{attacker} attempted to hit {target} with a roll of {roll}.\n"
ATTACK_FAILURE = ATTACK_COMMON + "The attack does not hit {target}."
ATTACK_FAILURE_TYPE_ERROR = ("Expected 'attacker', 'target', 'roll', "
                             "'health_left' and 'damage' in **kwargs.")
ATTACK_SUCCESS = (ATTACK_COMMON +
                  "The attack hits and deals {damage} damage.\n"
                  "{target} has {health_left} health remaining.")
ATTACK_SUCCESS_TYPE_ERROR = ("Expected 'attacker', 'target', "
                             "and 'roll' in **kwargs.")
COLLISION_MESSAGE = "Oh no, you can't move through walls, unless you're a ghost."
EXIT_MESSAGE = "Bye bye, hope you had a nice time in the sex dungeon!"
MENU_TEXT = """Controls:
'w' - move up
's' - move down
'a' - move left
'd' - move right
'x' - attack
'c' - cast spell
'q' - GTFO

What do you want to do:
"""
NO_ATTACK_MESSAGE = "WHY CHOOSE VIOLENCE?!?"
NO_MOVEMENT_MESSAGE = "Oh no, it seems you haven't learned how to move!"
NO_ONE_TO_PLAY_MESSAGE = "Well you don't have a character yet, do you?!"
NO_SPELLCASTING_MESSAGE = "Abracadabra. Nothing happens."


class Gui:
    def __init__(self):
        self._message_buffer = ""
    
    def add_attack_summary(self, success, **kwargs):
        """Add a summary of the attack to the message buffer.
        
        The function expects at least (on success=False):
         - attacker
         - target
         - roll
        
        And optionally (on success=True):
         - damage
         - health_left
        """
        message = ATTACK_SUCCESS if success else ATTACK_FAILURE
        try:
            self._message_buffer += message.format(**kwargs)
        except KeyError:
            fail_message = ATTACK_SUCCESS_TYPE_ERROR if success else ATTACK_FAILURE_TYPE_ERROR
            raise TypeError(fail_message)

    def add_message(self, message):
        """Add a simple message to the message buffer."""
        self._message_buffer += message

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def draw_screen(self, game_map):
        self.clear_screen()
        print(game_map)
        if self._message_buffer:
            print(self._message_buffer, end="\n\n")
            self._message_buffer = ""
        print(MENU_TEXT)
    
    def exit(self, message=EXIT_MESSAGE):
        print(message)
        sys.exit(0)