# -*- coding: utf-8 -*-

__author__ = 'Hans E Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

from biolab.simulation import Sim


def test_sim_create():
    n_dish = 5
    n_a = 10
    n_b = 20

    s = Sim(n_dish, n_a, n_b, 12345)
    data = s.run(cycles=0, return_counts=True)
    assert data.shape == (1, 3)

    c, tot_a, tot_b = data[0, :]
    assert c == 0
    assert tot_a == n_dish * n_a
    assert tot_b == n_dish * n_b

