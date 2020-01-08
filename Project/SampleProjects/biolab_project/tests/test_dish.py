# -*- coding: utf-8 -*-

__author__ = 'Hans E Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

import pytest
from scipy.stats import binom_test
from biolab.dish import Dish
from biolab.bacteria import Bacteria

# acceptance limit for statistical tests
ALPHA = 0.001

def test_dish_create():
    d = Dish(10, 20)
    assert d.get_num_a() == 10
    assert d.get_num_b() == 20


class TestAgingCalls(object):
    """
    Tests that Dish.aging() makes the correct number of calls
    to Bacteria.ages().
    """

    def test_dish_ages(self, mocker):
        # mocker.spy wraps Bacteria.ages() so that we can get
        # a call count (and more information if we wanted)
        mocker.spy(Bacteria, 'ages')

        n_a, n_b = 10, 20
        d = Dish(n_a, n_b)
        d.aging()

        assert Bacteria.ages.call_count == n_a + n_b

    def test_dish_ages_callers(self, mocker):
        # mocker.spy wraps Bacteria.ages() so that we can get
        # a list of arguments for all calls to ages()
        mocker.spy(Bacteria, 'ages')

        n_a, n_b = 10, 20
        d = Dish(n_a, n_b)
        d.aging()

        # get list of arguments for each call
        # each element of the list is a tuple: (positional_args, kwargs)
        # ages() takes only self as positional arg, so we are only
        # interested in those
        args = Bacteria.ages.call_args_list
        pos_args, kwargs = zip(*args)

        # pos_args should be n_a + n_b different bacteria objects
        # use set() to eliminate duplicates
        assert len(set(pos_args)) == len(pos_args)

    def test_zz_Bacteria_unaffected(self):
        """
        Confirm that the "spy" wrapper for Bacteria.ages is effective
        only in test_dish_ages(). This test is here only to confirm
        our understanding of the mocking mechanism.

        The name contains _zz_ to make sure this tests runs last,
        assuming that tests will be run in alphabetical order.
        """

        with pytest.raises(AttributeError):
            Bacteria.ages.call_count


class TestDeathDivision:
    """
    Tests for death and division.

    The main point of this test class is to show the use of a fixture
    to create an initial population before each test.
    """

    @pytest.fixture(autouse=True)
    def create_dish(self):
        self.n_a = 10
        self.n_b = 20
        self.dish = Dish(self.n_a, self.n_b)

    @pytest.fixture
    def p_death_one(self):
        # set death probability to 1 before test (setup)
        Bacteria.set_params({'p_death': 1})
        yield
        # code after yield executed after test (teardown)
        Bacteria.set_params(Bacteria.default_params)

    def test_death(self):
        # test of fixture: do we have a "fresh" dish?
        n_a_old = self.dish.get_num_a()
        n_b_old = self.dish.get_num_b()
        assert n_a_old == self.n_a
        assert n_b_old == self.n_b

        for _ in range(10):
            self.dish.death()
            n_a = self.dish.get_num_a()
            n_b = self.dish.get_num_b()
            assert n_a <= n_a_old
            assert n_b <= n_b_old
            n_a_old, n_b_old = n_a, n_b

        # after 10 rounds of death probability of no change is minimal
        assert self.dish.get_num_a() < self.n_a
        assert self.dish.get_num_b() < self.n_b


    def test_division(self):
        # test of fixture: do we have a "fresh" dish?
        n_a_old = self.dish.get_num_a()
        n_b_old = self.dish.get_num_b()
        assert n_a_old == self.n_a
        assert n_b_old == self.n_b

        for _ in range(10):
            self.dish.division()
            n_a = self.dish.get_num_a()
            n_b = self.dish.get_num_b()
            assert n_a >= n_a_old
            assert n_b >= n_b_old
            n_a_old, n_b_old = n_a, n_b

        # after 10 rounds of death probability of no change is minimal
        assert self.dish.get_num_a() > self.n_a
        assert self.dish.get_num_b() > self.n_b

    def test_all_die(self, p_death_one):
        self.dish.death()
        assert self.dish.get_num_a() == 0
        assert self.dish.get_num_b() == 0

    def test_zz_p_death_fine(self):
        """
        Test to check that p_death modified only in test_all_die.
        """
        assert Bacteria.p_death == Bacteria.default_params['p_death']


@pytest.mark.parametrize("n_a, n_b, p_death",
                         [[100, 200, 0.1],
                          [100, 200, 0.9],
                          [10, 20, 0.5]])
def test_death(n_a, n_b, p_death):
    Bacteria.set_params({'p_death': p_death})
    dish = Dish(n_a, n_b)
    dish.death()
    died_a = n_a - dish.get_num_a()
    died_b = n_b - dish.get_num_b()
    Bacteria.set_params(Bacteria.default_params)
    
    assert binom_test(died_a, n_a, p_death) > ALPHA
    assert binom_test(died_b, n_b, p_death) > ALPHA
