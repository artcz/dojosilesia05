# coding: utf-8

from random import randrange, choice
from base import BaseGame

RED = 8
ORANGE = 9
YELLOW = 10


MAX_WIDTH, MAX_HEIGHT = 10, 10
AVAILABLE_SHIP_LENGTHS = [2, 3, 4]


class DojoException(Exception):
    pass


class NotOnMapException(DojoException):
    pass


class Ship:

    def __init__(self, length):
        self.length = length
        self.positions = []


NORTH = (-1, 0)
EAST = (0, +1)
WEST = (0, -1)
SOUTH = (+1, 0)

board_state = {}


def is_on_map(x, y):
    return 0 <= x <= MAX_WIDTH and 0 <= y <= MAX_HEIGHT


def place_ship(ship_size):
    assert ship_size in AVAILABLE_SHIP_LENGTHS
    height, width = MAX_HEIGHT - ship_size, MAX_WIDTH - ship_size
    start_location = randrange(0, width), randrange(0, height)

    while True:
        direction = choice([NORTH, EAST, WEST, SOUTH])
        x, y = start_location
        locations = [(x, y)]

        try:
            for i in range(1, ship_size):
                x += direction[0]
                y += direction[1]

                if not is_on_map(x, y):
                    raise NotOnMapException()

                locations.append((x, y))
            else:
                return direction, locations
        except NotOnMapException:
            locations = []
            continue


def is_colliding(ship, board_state):
    for position in ship:
        try:
            if board_state.get(position, False):
                return True
        except TypeError:
            import pdb; pdb.set_trace()
    else:
        return False


def place_all_the_ships():
    sizes = [2, 2, 2, 3, 3, 4]
    i = 0
    ships = []
    while i < len(sizes):
        _, ship = place_ship(sizes[i])
        if is_colliding(ship, board_state):
            continue
        else:
            ships.append(ship)
            i += 1
            for s in ship:
                board_state[s] = True

    return ships



class Game(BaseGame):

    def __init__(self):
        super().__init__()
        self.clicks = 0

    def setup(self):
        pass

    def logic(self):
        pass

    def tick(self, mouse_x=0, mouse_y=0, is_clicked=False):
        # X is from 0 to 23
        # Y is from 0 to 17
        if is_clicked:
            self.clicks += 1
            self.logic()
            print(self.clicks, mouse_x, mouse_y)


    def draw_game(self, mouse_x=0, mouse_y=0):
        # X is from 0 to 23
        # Y is from 0 to 17
        self.draw.grid()

        # colors are descripted on https://github.com/kitao/pyxel#color-palette
        # self.draw.text(str, x, y, [color])
        self.draw.text('CODING DOJO', 2, 2, color=YELLOW)
        self.draw.text('SILESIA TEAM PYKONIK', 2, 3, color=YELLOW)

        # self.draw.image(name, x, y)
        # name = ship | selected_ship | miss | hit | cursor
        self.draw.image('ship', 5, 10)
        self.draw.image('selected_ship', 6, 10)
        self.draw.image('miss', 7, 10)
        self.draw.image('hit', 8, 10)
        self.draw.image('cursor', mouse_x, mouse_y)


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()

