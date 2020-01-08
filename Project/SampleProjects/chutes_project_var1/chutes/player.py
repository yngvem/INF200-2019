# -*- coding: utf-8 -*-

"""
This module provides classes implementing various Player types.
"""

import random

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


class Player(object):
    """
    Implements single player.
    """

    def __init__(self, board):
        """
        :param board: board on which player is living
        """
        self._board = board
        self.position = 0
        self.number_of_moves = 0

    def _move(self, extra_steps=0, min_steps=0):
        """
        Worker function moving player to new position.

        :param extra_steps: number of steps to add to die cast
        :param min_steps: never move fewer than this number forward
        :returns: position adjustment due to chute or ladder
        """

        self.position += max(min_steps, random.randint(1, 6) + extra_steps)
        adjustment = self._board.position_adjustment(self.position)
        self.position += adjustment
        self.number_of_moves += 1
        return adjustment

    def move(self):
        """
        Moves player to new position.
        """

        self._move()


class ResilientPlayer(Player):
    """
    Implements a player who makes extra efforts after sliding down.

    At the step after sliding down a slide, this player moves N extra
    squares at the next move.
    """

    def __init__(self, board, extra_steps=1):
        """
        :param extra_steps: number of extra steps on move after sliding down
        """

        Player.__init__(self, board)
        self.extra_steps = extra_steps
        self.went_down_in_last_move = False

    def move(self):
        extra = self.extra_steps if self.went_down_in_last_move else 0
        adjustment = self._move(extra)
        self.went_down_in_last_move = adjustment < 0


class LazyPlayer(Player):
    """
    Implements a player who makes a lesser effort after climbing up.

    At the step after climbing a slide, this player moves N fewer
    squares at the next move.
    """

    def __init__(self, board, dropped_steps=1):
        """
        :param dropped_steps: number of steps dropped after climbing up
        """

        Player.__init__(self, board)
        self.dropped_steps = dropped_steps
        self.climbed_in_last_move = False

    def move(self):
        dropped = self.dropped_steps if self.climbed_in_last_move else 0
        adjustment = self._move(-dropped)  # pass dropped steps as neg number
        self.climbed_in_last_move = adjustment > 0
