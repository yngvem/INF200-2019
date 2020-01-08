# -*- coding: utf-8 -*-

__author__ = 'Hans E Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

import random
import math
import pytest
import scipy.stats as stats

from biolab.bacteria import Bacteria

# Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests

@pytest.fixture
def set_params(request):
    """
    Fixture setting class parameters on Bacteria.

    The fixture sets Bacteria parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test.

    This fixture should be called via parametrize with indirect=True.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    ----------
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        Bacteria.set_params()
    """
    Bacteria.set_params(request.param)
    yield
    Bacteria.set_params(Bacteria.default_params)


def test_bact_create():
    """
    Test that a new bacterium has age 0.
    """
    b = Bacteria()
    assert b.age == 0


def test_bact_aging():
    """
    This test is *determinstic*: for each call to ages(),
    the age must increase by one year.
    """

    b = Bacteria()
    for n in range(10):
        b.ages()
        assert b.age == n + 1


@pytest.mark.parametrize('set_params', [{'p_death': 1.0}], indirect=True)
def test_bact_certain_death(set_params):
    """
    This test is *deterministic*: We set death probability to 1,
    thus the bacterium must always die. We call dies() multiple
    times to test this.

    Paramterization with a single-element list of parameter values will run
    this test once. Because we set `indirect=True`, Pytest will first invoke
    the set_params fixture defined above, passing the dictionary
    `{'p_death': 1.0}` as `request.param` to the fixture. The fixture then
    calls `Bacteria.set_params()` and also ensures clean-up after the test.
    """

    b = Bacteria()
    for _ in range(100):
        assert b.dies()


@pytest.mark.parametrize('set_params', [{'p_death': 0.0}], indirect=True)
def test_bact_certain_survival(set_params):
    """
    This test is *deterministic*: We set death probability to 0,
    thus the bacterium must never die. We call dies() multiple
    times to test this.
    """

    b = Bacteria()
    for _ in range(100):
        assert not b.dies()


@pytest.mark.parametrize('set_params', [{'p_death': 0.4}], indirect=True)
def test_bact_death_z_test(set_params):
    """
    This test is a probabilistic test: It executes dies() N times.
    The number n of "successes" (dies() returns True) should be
    distributed according to the binomial distribution B(N, p),
    where p is short for p_death. For large N, the distribution
    is approximately normal (law of large numbers) with mean
    Np and variance Np(1-p).

    Then, Z = ( n - Np ) / sqrt( N p (1-p) ) is distributed according
    to the normal distribution with mean 0 and variance 1. Thus,
    if dies() works correctly, we will observe Z < -Z* or Z > Z* only
    with probability Phi(-Z*) + ( 1-Phi(Z*) ) = 2 * Phi(-Z*), where
    equality follows from the symmetry of the normal distribution.
    This is the probability mass in the tails of the distribution.

    We can choose a signficance level alpha, e.g. 0.01, and
    pass the test if 2*Phi(-|Z|) > alpha: The test passes if the
    probability mass outside (-|Z], |Z]) is at least alpha (the
    observed value of Z is not in the alpha-tail of the distribution).
    """

    random.seed(SEED)
    N = 100
    p = Bacteria.get_params()['p_death']  # obtain parameter set by fixture

    b = Bacteria()
    n = sum(b.dies() for _ in range(N))  # True == 1, False == 0

    mean = N * p
    var = N * p * (1 - p)
    Z = (n - mean) / math.sqrt(var)
    phi = 2 * stats.norm.cdf(-abs(Z))
    assert phi > ALPHA


@pytest.mark.parametrize('key', ['p_death', ''
                                            'p_divide'])
def test_p_unchanged(key):
    """
    Ensure that class-level probabilities are unchanged by other tests.
    """
    assert getattr(Bacteria, key) == Bacteria.default_params[key]
