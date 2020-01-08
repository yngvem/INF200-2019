# -*- coding: utf-8 -*-

"""
To create a package, run

python setup.py sdist

in the directory containing this file.

To create a zip archive in addition to a tar.gz archive, run

python setup.py sdist --formats=gztar,zip

The package will be placed in directory dist.

To install from the package, unpack it, move into the unpacked directory and
run

python setup.py install          # default location
python setup.py install --user   # per-user default location

See also
    https://docs.python.org/3.6/distributing
    https://docs.python.org/3.6/installing
    https://packaging.python.org/tutorials/distributing-packages/
"""

from setuptools import setup
import codecs
import os

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'


def read_readme():
    """
    Read README.rst for use as long description.

    Based on PyPA Sample Project https://github.com/pypa/sampleproject

    :return: Multiline string containing contents of README.rst
    """

    # build absolute path to directory containing setup.py
    here = os.path.abspath(os.path.dirname(__file__))

    # read the README.rst file
    # using codes.open ensures that the file is read properly when using
    # UTF-8 encoding, e.g., for non-ASCII characters
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    return long_description


setup(
      # Basic information
      name='chutes',
      version='0.1.0',

      # Packages to include
      packages=['chutes'],

      # Required packages not included in Python standard library
      requires=['pytest'],

      # Metadata
      description='A Chutes & Ladders Simulation',
      long_description=read_readme(),
      author='Hans Ekkehard Plesser, NMBU',
      author_email='hans.ekkehard.plesser@nmbu.no',
      url='https://bitbucket.org/heplesser/nmbu_inf200_h18',
      keywords='simulation game',
      license='MIT License',
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Science :: Stochastic processes',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        ]
)
