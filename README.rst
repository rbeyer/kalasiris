=========
kalasiris
=========

*Calling ISIS programs from Python*

---------------------------------

.. image:: https://img.shields.io/pypi/v/kalasiris.svg
        :target: https://pypi.python.org/pypi/kalasiris

.. image:: https://img.shields.io/conda/vn/conda-forge/kalasiris.svg
        :target: https://anaconda.org/conda-forge/kalasiris

.. image:: https://travis-ci.com/rbeyer/kalasiris.svg?branch=master
        :target: https://travis-ci.com/rbeyer/kalasiris

.. image:: https://img.shields.io/circleci/project/github/conda-forge/kalasiris-feedstock/master.svg?label=noarch
        :target: https://circleci.com/gh/conda-forge/kalasiris-feedstock

.. image:: https://readthedocs.org/projects/kalasiris/badge/?version=latest
        :target: https://kalasiris.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


The *kalasiris* library is a Python library to wrap functions and
functionality for the `Integrated Software for Imagers and Spectrometers
(ISIS) <https://isis.astrogeology.usgs.gov>`_.


* Free software: Apache Software License 2.0
* Documentation: https://kalasiris.readthedocs.io.


WARNING
-------
**This is a very early development version, be warned!**


Features
--------

* Primarily a very lightweight wrapper around Python's subprocess
  module to allow easy calling of ISIS programs in the shell from
  within Python.
* Calling compatibility with pysis_ (but not return types)
* Guaranteed to work with ISIS 3.6.0+, probably works with ISIS 3+
* Only guaranteed to work with Python 3.6.0+


ISIS
----

This library really only works if you already have ISIS_ installed and
working properly.  Quirks of working with where and how ISIS is loaded
in your environment and how to use kalasiris with it, can be found
in the documentation.


Quickstart
----------

Are you new to Python?  Or you just don't want to mess with
sophisticated Python installation procedures?  Or you don't want
to commit to installing something when you don't know if it will
be worth it?  Or you just want to write something 'real quick' in
Python and need to call some ISIS programs **now**?

We've got you covered.

Just go into the ``kalasiris`` directory, and copy the ``kalasiris.py``
file into the same directory where your program is.  It doesn't
depend on anything that isn't already part of Python, so you can
just use it like so::

    from kalasiris import cam2map

    fromcube = 'something.cub'
    tocube = 'something_mapped.cub'
    cam2map(fromcube, to=mapfile)

Easy! Assuming you have a ``something.cub`` file that can be
map-projected.

Just grabbing this one file gets you the ability to call ISIS
programs from your Python programs.  There are other parts of this
package that provide helper functions (like ``cubenormDialect``),
classes (like ``Histogram``), and syntactic sugar (the *_k functions*).
You don't get them by just grabbing ``kalasiris.py`` as described
above.

If you want *all* of the kalasiris library, but still don't want to
go through some formal installation process, you can clone this repo,
and then move (or copy) the whole ``kalasiris/`` directory (instead
of just the ``kalasiris.py`` file inside of it) to your project, and
then do the same thing as above, but now you can do more fun things
like this::

    import kalasiris as isis

    img      = 'PSP_010502_2090_RED5_0.IMG'
    hicube   = 'PSP_010502_2090_RED5_0.cub'
    histfile = 'PSP_010502_2090_RED5_0.hist'

    isis.hi2isis(img, to=hicube)

    InsID = isis.getkey_k(hicub, 'Instrument', 'InstrumentId')
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


You can see that you now have access to things like the Histogram class,
the ``getkey_k()`` *_k function*, and much more.

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


-------

This repository layout was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _ISIS: https://isis.astrogeology.usgs.gov
.. _pysis: https://github.com/wtolson/pysis
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
