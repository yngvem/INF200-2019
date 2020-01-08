#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a small demo script running a ranvis simulation.
"""

__author__ = "Hans E Plesser / NMBU"

import matplotlib.pyplot as plt
from randvis.simulation import DVSim

if __name__ == '__main__':

    sim = DVSim((10, 15), 0.1, 12345)
    sim.simulate(50, 1, 5)

    input('Press ENTER to simulate some more!')

    sim.simulate(100, 1, 5)

    print('Close the figure to end the program!')

    plt.show()
