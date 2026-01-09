"""
Labyrinth Game - Текстовый квест
"""

__version__ = "0.1.0"
__author__ = "Shicimiki"

from labyrinth_game.constants import ROOMS, COMMANDS
from labyrinth_game.player_actions import (
    get_input, move_player, take_item, 
    show_inventory, use_item
)
from labyrinth_game.utils import (
    describe_current_room, solve_puzzle,
    attempt_open_treasure, show_help
)
