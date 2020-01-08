# -*- coding: utf-8 -*-

"""
Implements a complete simulation.
"""

import numpy as np
import random
from .laboratory import Lab
from .bacteria import Bacteria


class Sim:
    """Define and perform a simulation."""

    def __init__(self, n_dishes, n_a, n_b, seed, p_dth=0.1, p_div=0.1):
        """
        Parameters
        ----------
        n_dishes : int
            number of Petri dishes in lab
        n_a : int
            number of bacteria of type A per dish
        n_b : int
            number of bacteria of type B per dish
        seed : int
            random seed
        p_dth : float
            death probability per cycle
        p_div : float
            division probability per cycle
        """

        random.seed(seed)
        Bacteria.set_params({'p_death': p_dth,
                             'p_divide': p_div})
        self.lab = Lab(n_dishes, n_a, n_b)

    def run(self, cycles, report_cycles=1, return_counts=False):
        """
        Run simulation for given number of cycles.

        Parameters
        ----------
        cycles : int
            number of cycles to simulate
        report_cycles : int
            interval between status information updates (== 0: no output)
        return_counts : int
            if True, return population counts
        Returns
        -------
        None or tuple
            If return of counts is requested, a tuple (cycle, nA, nB)
        """

        disp = report_cycles > 0
        ret = return_counts

        if ret:
            data = np.empty((cycles + 1, 3))
            data[:, 0] = range(cycles + 1)
            data[0, 1:] = self.lab.bacteria_counts()
        else:
            data = None

        if disp:
            print('Start:', self.lab.bacteria_counts())

        for cycle in range(cycles):
            self.lab.cycle()
            disp_this_cycle = disp and cycle % report_cycles == 0

            if ret or disp_this_cycle:
                n_a, n_b = self.lab.bacteria_counts()
            if ret:
                data[cycle + 1, 1:] = n_a, n_b
            if disp_this_cycle:
                print(n_a, n_b)

        if disp:
            print('End: ', self.lab.bacteria_counts())

        if ret:
            return data
