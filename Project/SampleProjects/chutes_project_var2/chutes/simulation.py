# -*- coding: utf-8 -*-

"""
This module provides classes organizing entire simulation experiments.
"""

import copy
import random
from .board import Board

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


class Simulation(object):
    """
    Implements a complete Chutes & Ladders simulation.
    """

    def __init__(self, player_field, board=None, seed=1234567,
                 randomize_players=False):
        """
        :param player_field: list of player classes or prototype instances
        :param board: Board instance (default: standard board)
        :param seed: random generator seed
        :param randomize_players: randomize player order at start of game
        """

        self._board = board if board is not None else Board()

        # player_field can contain a mix of player classes and instances
        # create a prototype instances where necessary
        self._player_prototypes = [player(self._board)
                                   if isinstance(player, type) else player
                                   for player in player_field]
        self._player_types = frozenset(type(player)
                                       for player in self._player_prototypes)
        self._results = []
        self._randomize = randomize_players

        random.seed(seed)

    def single_game(self):
        """
        Returns winner type and number of steps for single game.

        :returns: (number_of_steps, winner_class) tuple
        """

        # create players as copies of prototypes
        players = [copy.copy(player) for player in self._player_prototypes]
        if self._randomize:
            random.shuffle(players)

        while True:
            for player in players:
                player.move()
                if self._board.goal_reached(player.position):
                    return player.number_of_moves, player.__class__

    def run_simulation(self, num_games):
        """
        Run a set of games, store results in Simulation.

        If results exist from before, new data will be added to existing data.

        :param num_games: number of games to play
        """

        # Using a loop here allows us to add progress information printout
        for _ in range(num_games):
            self._results.append(self.single_game())

    def players_per_type(self):
        """
        Returns a dict mapping player classes to number of players.
        """

        all_player_types = [type(player) for player in self._player_prototypes]
        return {player_type: all_player_types.count(player_type)
                for player_type in self._player_types}

    def winners_per_type(self):
        """
        Returns dict showing number of winners for each type of player.
        """

        winner_types = list(zip(*self._results))[1]
        return {player_type: winner_types.count(player_type)
                for player_type in self._player_types}

    def durations_per_type(self):
        """
        Returns dict mapping winner type to list of game durations for type.
        """

        return {player_type: [duration for duration, winner_type
                              in self._results
                              if winner_type == player_type]
                for player_type in self._player_types}
