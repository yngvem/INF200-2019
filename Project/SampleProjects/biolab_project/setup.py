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
python setup.py install --prefix=/Users/plesser/tmp/test  # to given dir
"""

from distutils.core import setup

setup(
      name='BioLab',
      version='0.1',
      description='A Cell Laboratory Simulation',
      author='Hans E Plesser, NMBU',
      author_email='hans.ekkehard.plesser@nmbu.no',
      url='http://arken.nmbu.no/~plesser',
      requires=['numpy (>=1.8.1)', 'matplotlib (>= 1.3.1)'],
      packages=['biolab', 'biolab.tests'],
)
