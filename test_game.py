from game import (
    Game,
    is_on_map,
    place_ship,
    place_all_the_ships,
    YELLOW,
    AVAILABLE_SHIP_LENGTHS,
    NORTH, EAST, WEST, SOUTH,
    SHIP_SIZES,
)

from base import Drawer

from unittest.mock import Mock, call
import pytest


def test_place_ship_returns_a_valid_ship():
    ship_size = 3
    direction, locations = place_ship(ship_size)
    assert direction in {NORTH, EAST, WEST, SOUTH}

    # check if ship is a single unit
    for l1, l2 in zip(locations, locations[1:]):
        if direction in {NORTH, SOUTH}:
            assert abs(l1[0] - l2[0]) == 1
            assert l1[1] == l2[1]

        if direction in {EAST, WEST}:
            assert l1[0] == l2[0]
            assert abs(l1[1] - l2[1]) == 1

    for location in locations:
        assert is_on_map(*location)


@pytest.mark.parametrize("size,expected", [
    (2, 2),
    (3, 3),
    (4, 4),
])
def test_place_ship_output(size, expected):
    direction, locations = place_ship(size)
    assert len(locations) == expected


def test_place_all_the_ships():
    ships = place_all_the_ships()
    assert len(ships) == len(SHIP_SIZES)
    for ship, ship_size in zip(ships, SHIP_SIZES):
        assert len(ship) == ship_size


def get_game(*args, **kwargs):
    game = Game(*args, **kwargs)
    game.draw = Mock(spec=Drawer)
    return game


def test_tick():
    game = get_game()
    game.tick(is_clicked=True)

    assert game.clicks == 1


def test_draw():
    game = get_game()
    game.draw_game(mouse_x=5, mouse_y=5)

    # more info about mocks:
    # https://docs.python.org/3/library/unittest.mock.html
    game.draw.grid.assert_called_once_with()
    assert game.draw.text.call_args_list == [
        call('CODING DOJO', 2, 2, color=YELLOW),
        call('SILESIA TEAM PYKONIK', 2, 3, color=YELLOW),
    ]

    assert game.draw.image.call_args_list == [
        call('ship', 5, 10),
        call('selected_ship', 6, 10),
        call('miss', 7, 10),
        call('hit', 8, 10),
        call('cursor', 5, 5),
    ]
