# -*- coding: utf-8 -*-

"""
Tests for Board class.
"""

import pytest

from chutes.board import Board

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


def test_goal_not_reached():
    """"Ensure goal_reached() does not yield false positives."""
    goal_pos = 20
    brd = Board(ladders=[], chutes=[], goal=goal_pos)
    for pos in range(goal_pos):
        assert not brd.goal_reached(pos)


def test_goal_reached():
    """Ensure goal_reached() does not yield false negatives."""
    goal_pos = 20
    brd = Board(ladders=[], chutes=[], goal=goal_pos)
    for pos in range(goal_pos, goal_pos+10):
        assert brd.goal_reached(pos)


def test_adjust_empty_board():
    """"No position adjustment on empty board."""

    goal_pos = 20
    brd = Board(ladders=[], chutes=[], goal=goal_pos)
    for pos in range(goal_pos):
        assert brd.position_adjustment(pos) == 0


def test_adjustment():
    goal_pos = 20
    ladders = [(2, 10), (9, 13), (12, 18)]
    chutes = [(4, 1), (7, 3), (17, 8)]
    test_cases = {0: 0, 1: 0, 2: 8, 3: 0, 4: -3, 5: 0, 6: 0, 7: -4,
                  8: 0, 9: 4, 10: 0, 11: 0, 12: 6, 13: 0, 14: 0,
                  15: 0, 16: 0, 17: -9, 18: 0, 19: 0}
    brd = Board(ladders=ladders, chutes=chutes, goal=goal_pos)
    for pos, change in test_cases.items():
        assert brd.position_adjustment(pos) == change


def test_default_board():
    """Some tests on default board."""

    brd = Board()
    assert brd.position_adjustment(1) == 39
    assert brd.position_adjustment(2) == 0
    assert brd.position_adjustment(33) == -30
    assert not brd.goal_reached(89)
    assert brd.goal_reached(90)
    assert brd.goal_reached(91)


def test_bad_boards():
    """Test that bad board specifications are not accepted."""

    with pytest.raises(ValueError):
        Board(ladders=[(10, 10)])

    with pytest.raises(ValueError):
        Board(ladders=[(10, 9)])

    with pytest.raises(ValueError):
        Board(chutes=[(10, 10)])

    with pytest.raises(ValueError):
        Board(chutes=[(10, 12)])

    with pytest.raises(ValueError):
        Board(goal=0)
