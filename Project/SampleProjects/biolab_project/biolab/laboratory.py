# -*- coding: utf-8 -*-

"""
Implements a laboratory with many dishes.
"""

from .dish import Dish


class Lab:
    """A laboratory with many dishes."""

    def __init__(self, n_dishes, n_bact_a, n_bact_b):
        """
        Parameters
        ----------
        n_dishes : int
            number of Petri dishes in lab
        n_bact_a : int
            number of bacteria of type A per dish
        n_bact_b : int
            number of bacteria of type B per dish
        """

        self.dishes = [Dish(n_bact_a, n_bact_b) for _ in range(n_dishes)]

    def cycle(self):
        """Update all dishes by one cycle."""

        for dish in self.dishes:
            dish.aging()
            dish.death()
            dish.division()

    def bacteria_counts(self):
        """
        Count bacteria across dishes.

        Returns
        -------
        tuple
            Two-element tuple with count of A and B bacteria.
        """

        return (sum(d.get_num_a() for d in self.dishes),
                sum(d.get_num_b() for d in self.dishes))
