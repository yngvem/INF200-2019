# -*- coding: utf-8 -*-

"""
Script demonstrating the use of the chutes package.
"""

from chutes.simulation import Simulation
from chutes.board import Board
from chutes.player import *
from chutes.helpers import type_to_name

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

print('**** First Simulation: Single player, standard board ****')
sim = Simulation([Player])
print(type_to_name(sim.single_game()))

sim.run_simulation(10)
print(type_to_name(sim.players_per_type()))
print(type_to_name(sim.winners_per_type()))
print(type_to_name(sim.durations_per_type()))

print('\n**** Second Simulation: Four players, standard board ****')
sim = Simulation([Player, Player, LazyPlayer, ResilientPlayer])
print(type_to_name(sim.single_game()))

sim.run_simulation(10)
print(type_to_name(sim.players_per_type()))
print(type_to_name(sim.winners_per_type()))
print(type_to_name(sim.durations_per_type()))

print('\n**** Third Simulation: Four players, small board ****')
my_board = Board(ladders=[(3, 10), (5, 8)], chutes=[(9, 2)], goal=20)
sim = Simulation([Player, Player, LazyPlayer, ResilientPlayer],
                 board=my_board)
print(type_to_name(sim.single_game()))

sim.run_simulation(10)
print(type_to_name(sim.players_per_type()))
print(type_to_name(sim.winners_per_type()))
print(type_to_name(sim.durations_per_type()))

print('\n**** Fourth Simulation: Modified players, standard board ****')
board = Board()
sim = Simulation([Player(board),
                  LazyPlayer(board, dropped_steps=5),
                  ResilientPlayer(board, extra_steps=5)],
                 board=board)
print(type_to_name(sim.single_game()))

sim.run_simulation(10)
print(type_to_name(sim.players_per_type()))
print(type_to_name(sim.winners_per_type()))
print(type_to_name(sim.durations_per_type()))
