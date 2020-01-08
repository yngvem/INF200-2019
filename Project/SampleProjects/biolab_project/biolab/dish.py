# -*- coding: utf-8 -*-

"""
Implements a dish with bacteria cultures.
"""

from .bacteria import Bacteria


class Dish:
    """Petri dish containing bacteria of types A and B."""

    def __init__(self, num_a, num_b):
        """
        Parameters
        ----------
        num_a : int
            number of bacteria of type A in dish
        num_b : int
            number of bacteria of type A in dish
        """

        self.a_pop = [Bacteria() for _ in range(num_a)]
        self.b_pop = [Bacteria() for _ in range(num_b)]

    def get_num_a(self):
        """Return number of A bacteria in dish."""

        return len(self.a_pop)

    def get_num_b(self):
        """Return number of B bacteria in dish."""

        return len(self.b_pop)

    def aging(self):
        """Age all bacteria in dish by one cycle."""

        for bact in self.a_pop + self.b_pop:
            bact.ages()

    def death(self):
        """Remove dying bacteria."""

        def survivors(pop):
            return [bact for bact in pop if not bact.dies()]

        self.a_pop = survivors(self.a_pop)
        self.b_pop = survivors(self.b_pop)

    def division(self):
        """For each dividing bacterium, add one new."""

        def newborns(pop):
            return [Bacteria() for parent in pop if parent.divides()]

        self.a_pop.extend(newborns(self.a_pop))
        self.b_pop.extend(newborns(self.b_pop))

