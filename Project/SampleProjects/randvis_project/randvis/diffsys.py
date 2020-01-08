# -*- coding: utf-8 -*-

'''
:mod:`randvis.diffsys` implements the simulated system.

The simulated system is very simple. At each step

#. each matrix element is replaced by the average of its own value and that
   of its right-hand neighbor;
#. a random value is added to each matrix element;
#. periodic boundary conditions are used, i.e., the leftmost column in the
   matrix is considered to be the right-hand neighbor of the rightmost column.
'''

__author__ = "Hans E Plesser, NMBU"

import numpy as np


class DiffSys(object):
    """Represents the system under simulation."""

    def __init__(self, syssize, noiselevel):
        """
        :param syssize: system size, (rows, columns)
        :param noiselevel: add uniform noise
                           from [-noiselevel/2, noiselevel/2)
        """

        if any(elem < 1 for elem in syssize):
            raise ValueError("System size must be strictly positive.")
        self._rows, self._cols = syssize

        if noiselevel < 0:
            raise ValueError("Noise level cannot be negative.")

        self._noise = noiselevel
        self._system = self._noise_matrix()

        # This index allows adding the value of the right neighbor
        # with periodic boundary conditions when used as
        # self._system[:, _idx] += self._system
        self._idx = np.arange(-1, self._cols - 1)

    def _noise_matrix(self):
        """Random matrix of system size values in [-noise/2, noise/2)"""

        return self._noise * (np.random.rand(self._rows, self._cols)
                              - 0.5)

    def update(self):
        """Advances system state."""

        self._system[:, self._idx] += self._system
        self._system *= 0.5
        self._system += self._noise_matrix()

    def mean_value(self):
        """Returns mean value of system elements."""

        return self._system.mean()

    def get_status(self):
        """Returns full data matrix."""

        return self._system
