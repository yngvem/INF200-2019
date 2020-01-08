# -*- coding: utf-8 -*-

"""
This file contains a very basic test only for demonstration.
"""

import numpy as np

from randvis.diffsys import DiffSys


def test_create_no_noise():
    ds = DiffSys([1, 1], 0.)
    np.testing.assert_array_equal(ds.get_status(), np.zeros([1, 1]))

    ds = DiffSys([2, 3], 0.)
    np.testing.assert_array_equal(ds.get_status(), np.zeros([2, 3]))
