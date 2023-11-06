import os


def draw_map(game_map):
    clear_screen()
    print(game_map.map)


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

