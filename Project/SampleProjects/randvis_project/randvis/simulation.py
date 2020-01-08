# -*- coding: utf-8 -*-

'''
:mod:`randvis.simulation` provides the user interface to the package.

Each simulation is represented by a :class:`DVSim` instance. On each
instance, the :meth:`DVSim.simulate` method can be called as often as
you like to simulate a given number of steps.

The state of the system is visualized as the simulation runs, at intervals
that can be chosen. The graphics can also be saved to file at regular
intervals. By calling :meth:`DVSim.make_movie` after a simulation is complete,
individual graphics files can be combined into an animation.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<http://ffmpeg.org>` and `<http://imagemagick.org>`.
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

Example
--------
::

    sim = DVSim((10, 15), 0.1, 12345, _DEFAULT_FILEBASE)
    sim.simulate(50, 1, 5)
    sim.make_movie()

This code

#. creates a system with a 10x15 matrix, sets the noise level to 0.1,
   the random number generator seed to 12345 and specifies the filename
   for output;
#. performs a simulation of 50 steps, updating the graphics after each
   step and saving a figure after each 5th step;
#. creates a movie from the individual figures saved.

'''

__author__ = "Hans E Plesser, NMBU"

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os
from randvis.diffsys import DiffSys

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class DVSim(object):
    """Provides user interface for simulation, including visualization."""

    def __init__(self, sys_size, noise, seed,
                 img_dir=None, img_name=_DEFAULT_GRAPHICS_NAME,
                 img_fmt='png'):
        """
        :param sys_size:  system size, e.g. (5, 10)
        :type sys_size: (int, int)
        :param noise: noise level
        :type noise: float
        :param seed: random generator seed
        :type seed: int
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix, default 'png'
        :type img_fmt: str
        """

        np.random.seed(seed)
        self._system = DiffSys(sys_size, noise)

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None
        self._img_fmt = img_fmt

        self._step = 0
        self._final_step = None
        self._img_ctr = 0

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._mean_line = None

    def simulate(self, num_steps, vis_steps=1, img_steps=None):
        """
        Run simulation while visualizing the result.

        :param num_steps: number of simulation steps to execute
        :param vis_steps: interval between visualization updates
        :param img_steps: interval between visualizations saved to files
                          (default: vis_steps)

        .. note:: Image files will be numbered consecutively.
        """

        if img_steps is None:
            img_steps = vis_steps

        self._final_step = self._step + num_steps
        self._setup_graphics()

        while self._step < self._final_step:

            if self._step % vis_steps == 0:
                self._update_graphics()

            if self._step % img_steps == 0:
                self._save_graphics()

            self._system.update()
            self._step += 1

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def _setup_graphics(self):
        """Creates subplots."""

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(1, 2, 1)
            self._img_axis = None

        # Add right subplot for line graph of mean.
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(1, 2, 2)
            self._mean_ax.set_ylim(0, 0.02)

        # needs updating on subsequent calls to simulate()
        self._mean_ax.set_xlim(0, self._final_step + 1)

        if self._mean_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, self._final_step),
                                           np.full(self._final_step, np.nan))
            self._mean_line = mean_plot[0]
        else:
            xdata, ydata = self._mean_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._mean_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))

    def _update_system_map(self, sys_map):
        '''Update the 2D-view of the system.'''

        if self._img_axis is not None:
            self._img_axis.set_data(sys_map)
        else:
            self._img_axis = self._map_ax.imshow(sys_map,
                                                 interpolation='nearest',
                                                 vmin=0, vmax=1)
            plt.colorbar(self._img_axis, ax=self._map_ax,
                         orientation='horizontal')

    def _update_mean_graph(self, mean):
        ydata = self._mean_line.get_ydata()
        ydata[self._step] = mean
        self._mean_line.set_ydata(ydata)

    def _update_graphics(self):
        """Updates graphics with current data."""

        self._update_system_map(self._system.get_status())
        self._update_mean_graph(self._system.mean_value())
        plt.pause(1e-6)

    def _save_graphics(self):
        """Saves graphics to file if file name given."""

        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
