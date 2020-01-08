# -*- coding: utf-8 -*-

'''
An minimal example of a BioLab simulation experiment.
'''

from biolab.simulation import Sim

if __name__ == '__main__':

    sim = Sim(n_dishes=3, n_a=20, n_b=10, seed=1234567,
              p_dth=0.05, p_div=0.05)
    sim.run(cycles=20)
