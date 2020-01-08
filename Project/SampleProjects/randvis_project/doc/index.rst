.. RandVis documentation master file, created by
   sphinx-quickstart on Sun Jan  6 10:47:09 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to RandVis's documentation!
===================================

RandomVisualization is a small Python package developed solely for pedagogical purposes.
The key points illustrated are how to

* visualize matrices using :func:`matplotlib.pyplot.imshow`
* create a video from saved graphics files using `FFmpeg <http://ffmpeg.org>`_
* provide a :class:`simulation` that provides a user interface to the simulated system
* document code with `Sphinx <http://sphinx-doc.org>`_
* create a distributable package using Python :mod:`distutils`

The package does nothing meaningful, it just generates a random matrix, modifies that
matrix for each simulation step and displays the resulting matrix and mean element 
value at given intervals. 

Contents:

.. toctree::
   :maxdepth: 2

   user_interface
   system


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

