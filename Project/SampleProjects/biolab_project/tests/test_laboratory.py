# -*- coding: utf-8 -*-

__author__ = 'Hans E Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

from biolab.laboratory import Lab


def test_lab_create():
    n_dish = 5
    n_a = 10
    n_b = 20
    l = Lab(n_dish, n_a, n_b)
    tot_a, tot_b = l.bacteria_counts()

    assert tot_a == n_dish * n_a
    assert tot_b == n_dish * n_b
