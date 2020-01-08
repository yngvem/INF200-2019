'''
Setup file for RandVis package.

To create a package, run

python setup.py sdist

in the directory containing this file.

To create a zip archive, run

python setup.py sdist --formats=zip

The package will be placed in directory dist.

To install from the package, unpack it, move into the unpacked directory and
run

python setup.py install          # default location
python setup.py install --user   # per-user default location

See also
    http://docs.python.org/distutils
    http://docs.python.org/install
    http://guide.python-distribute.org/creation.html

'''

__author__ = "Hans E Plesser, UMB"

from distutils.core import setup

setup(name='RandVis',
      version='0.1',
      description='A Meaningless Simulation for Demo Purposes.',
      author='Hans E Plesser, NMBU',
      author_email='hans.ekkehard.plesser@nmbu.no',
      requires=['numpy (>=1.6.1)',
                'matplotlib (>=1.1.0)'],
      packages=['randvis', 'randvis.tests'],
      scripts=['examples/rv_demo.py', 'examples/rv_demo.py'],
      )
