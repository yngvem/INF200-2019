# -*- coding: utf-8 -*-

"""
Tests for Player class.
"""

import pytest

from chutes.player import Player, LazyPlayer, ResilientPlayer
from chutes.board import Board
import random
import unittest.mock as mock

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


def test_single_step_one(mocker):
    '''
    Use mocked randint to test that a player makes a correct initial step
    of length 1.
    '''

    # the next line replaces random.randint with a mock function
    # returning 1 for the rest of this test.
    mocker.patch('random.randint', return_value=1)

    b = Board(chutes=[], ladders=[])
    pl = Player(b)
    pl.move()
    assert pl.position == 1


def test_multi_step_three(mocker):
    '''
    Use mocked randint to test that player makes multiple moves
    of given length.
    '''

    n_steps = 5
    randint_value = 3

    # the next line replaces random.randint with a mock function
    # returning randint_value for the rest of this test.
    mocker.patch('random.randint', return_value=randint_value)
    b = Board(chutes=[], ladders=[])
    pl = Player(b)
    for _ in range(n_steps):
        pl.move()

    assert pl.position == n_steps * randint_value

    # Check that random.randint was called once per call to move()
    # with arguments 1 and 6.
    assert random.randint.mock_calls == n_steps * [mock.call(1, 6)]
