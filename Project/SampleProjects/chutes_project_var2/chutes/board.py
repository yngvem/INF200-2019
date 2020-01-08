# -*- coding: utf-8 -*-

"""
This module provides classes implementing game boards for Chutes & Ladders.
"""

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


class Board(object):
    """
    Represents game board.

    This class provides a board of 90 squares (Egmont Libor AS, Oslo, 2001).
    """

    # Default board configuration
    DEFAULT_LADDERS = [(1, 40), (8, 10), (36, 52), (43, 62), (49, 79),
                       (65, 82), (68, 85)]
    DEFAULT_CHUTES = [(24, 5), (33, 3), (42, 30), (56, 37), (64, 27),
                      (74, 12), (87, 70)]
    DEFAULT_GOAL = 90

    def __init__(self, ladders=None, chutes=None, goal=None):
        """
        :param ladders: list of (start, end) tuples representing ladders
        :param chutes: list of (start, end) tuples representing chutes
        :param goal: destination square
        """

        if ladders is None:
            ladders = Board.DEFAULT_LADDERS
        if chutes is None:
            chutes = Board.DEFAULT_CHUTES
        for start, destination in ladders:
            if destination <= start:
                raise ValueError("Invalid ladder {} -> {}".format(start,
                                                                  destination))
        for start, destination in chutes:
            if destination >= start:
                raise ValueError("Invalid chute {} -> {}".format(start,
                                                                 destination))

        self._chutes_and_ladders = {start: end
                                    for start, end in chutes + ladders}
        self._goal = Board.DEFAULT_GOAL if goal is None else goal

        if self._goal <= 0:
            raise ValueError("Invalid goal, must be beyond start.")

    def goal_reached(self, position):
        """
        Returns True if player has reached goal.

        :param position: Player position
        """

        return position >= self._goal

    def position_adjustment(self, position):
        """
        Return change to position due to chute or ladder.

        If the player is not at the start of a chute/ladder, it returns 0.

        :param position: Player position
        :returns: number of fields player must move to get to correct position
        """

        # get() looks up a possible chute or ladder beginning at position.
        # If there is none, get() will return position instead.
        new_position = self._chutes_and_ladders.get(position, position)

        return new_position - position
