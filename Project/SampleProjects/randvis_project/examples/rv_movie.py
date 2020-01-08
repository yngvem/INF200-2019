#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a small demo script running a ranvis simulation and generating a movie.
"""

__author__ = "Hans E Plesser / NMBU"

from randvis.simulation import DVSim

sim = DVSim((10, 15), 0.1, 12345, '../data')
sim.simulate(100, 1, 5)
sim.make_movie('mp4')
sim.make_movie('gif')
