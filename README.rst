=========
kalasiris
=========

*Calling ISIS programs from Python*

---------------------------------

.. image:: https://img.shields.io/pypi/v/kalasiris.svg
        :target: https://pypi.python.org/pypi/kalasiris

.. image:: https://img.shields.io/conda/vn/conda-forge/kalasiris.svg
        :target: https://anaconda.org/conda-forge/kalasiris

.. image:: https://github.com/rbeyer/kalasiris/workflows/Python%20Testing/badge.svg
        :target: https://github.com/rbeyer/kalasiris/actions

.. image:: https://img.shields.io/circleci/project/github/conda-forge/kalasiris-feedstock/master.svg?label=noarch
        :target: https://circleci.com/gh/conda-forge/kalasiris-feedstock

.. image:: https://readthedocs.org/projects/kalasiris/badge/?version=latest
        :target: https://kalasiris.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://codecov.io/gh/rbeyer/kalasiris/branch/main/graph/badge.svg?token=TL5UZUQHRC
        :target: https://codecov.io/gh/rbeyer/kalasiris
        :alt: Codecov Status



The *kalasiris* library is a Python library to wrap functions and
functionality for the `Integrated Software for Imagers and Spectrometers
(ISIS) <https://isis.astrogeology.usgs.gov>`_.


* Free software: BSD-3-Clause License
* Documentation: https://kalasiris.readthedocs.io.


Features
--------

* Primarily a very lightweight wrapper around Python's subprocess
  module to allow easy calling of ISIS programs in the shell from
  within Python.
* Calling compatibility with pysis_ (and emulation of return types)
* Works with ISIS 3.6.0 and higher.
* Works with Python 3.6.0 and higher.


ISIS
----

This library really only works if you already have ISIS_ installed and
working properly.  Quirks of working with where and how ISIS is loaded
in your environment and how to use kalasiris with it, can be found
in the documentation.


Citing in your work
-------------------

Beyer, R. A. 2020. Kalasiris, a Python Library for Calling ISIS
Programs. 51st Lunar and Planetary Science Conference, not held due
to COVID-19, Abstract #2441. `ADS URL
<https://ui.adsabs.harvard.edu/abs/2020LPI....51.2441B>`_


Quickstart
----------

Are you new to Python? Do you just want to write something 'real quick'
in Python and need to call some ISIS programs **now**?

We've got you covered.

Need to run an ISIS program like ``cam2map``::

    from kalasiris import cam2map

    fromcube = 'something.cub'
    tocube = 'something_mapped.cub'
    cam2map(fromcube, to=tocube)

Easy! Assuming you have a ``something.cub`` file that can be
map-projected.  The first positional argument will be assumed to be
the "from" parameter, but you could also explicitly use ``from=fromcube``
here.

In addition to just calling *all* ISIS programs this way, you can do
other fun things like this::

    import kalasiris as isis

    img      = 'PSP_010502_2090_RED5_0.IMG'
    hicube   = 'PSP_010502_2090_RED5_0.cub'
    histfile = 'PSP_010502_2090_RED5_0.hist'

    isis.hi2isis(img, to=hicube)

    InsID = isis.getkey_k(hicube, 'Instrument', 'InstrumentId')
    print(InsID)
    # prints HIRISE

    isis.hist(hicube, to=histfile)

    h = isis.Histogram(histfile)

    print(h)
    # prints the hist file header info

    print(h['Std Deviation'])
    # prints 166.739

    print(h[1])
    # prints the second row of the histogram:
    # HistRow(DN=3924.0, Pixels=1.0, CumulativePixels=2.0, Percent=4.88281e-05, CumulativePercent=9.76563e-05)

    print(h[1][3])
    print(h[1].Percent)
    # both of the above print 4.88281e-05


You can see that there are things like the Histogram class,
the ``getkey_k()`` function which is part of the *_k function* collection, and much more.

Read the documentation for more: https://kalasiris.readthedocs.io


Installation
------------

You can install ``kalasiris`` via ``pip`` or ``conda-forge``:

To install ``kalasiris`` via ``pip``, run this command in your terminal:

.. code-block:: console

    $ pip install kalasiris

Installing ``kalasiris`` from the ``conda-forge`` channel can be
achieved by adding ``conda-forge`` to your channels with:

.. code-block:: console

    conda config --add channels conda-forge

Once the ``conda-forge`` channel has been enabled, ``kalasiris`` can be installed with:

.. code-block:: console

    conda install kalasiris

It is possible to list all of the versions of ``kalasiris`` available on your platform with:

.. code-block:: console

    conda search kalasiris --channel conda-forge


If for some reason you don't want to use conda or pip, you could do one of these
two things (but really, just use conda or pip):

The core functionality is contained in a single file.  Just go into the
``kalasiris`` directory, and copy the ``kalasiris.py``
file into the same directory where your own program is.  It doesn't
depend on anything that isn't already part of Python, so you can
just use it.

Just grabbing this one file gets you the ability to call ISIS
programs from your Python programs.  There are other parts of this
package that provide helper functions (like ``cubenormfile.writer``),
classes (like ``Histogram``), and syntactic sugar (the *_k functions*).
You don't get them by just grabbing ``kalasiris.py`` as described
above.

However, installation via pip or conda is so easy, and you're installing
ISIS via conda already.

-------

This repository layout was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _ISIS: https://isis.astrogeology.usgs.gov
.. _pysis: https://github.com/wtolson/pysis
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
