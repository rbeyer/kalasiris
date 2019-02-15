=========
kalasiris
=========


.. image:: https://img.shields.io/pypi/v/kalasiris.svg
        :target: https://pypi.python.org/pypi/kalasiris

.. image:: https://img.shields.io/travis/rbeyer/kalasiris.svg
        :target: https://travis-ci.org/rbeyer/kalasiris

.. image:: https://readthedocs.org/projects/kalasiris/badge/?version=latest
        :target: https://kalasiris.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



A Python library to wrap functions and functionality for the
`Integrated Software for Imagers and Spectrometers (ISIS)
<https://isis.astrogeology.usgs.gov>`_.


* Free software: Apache Software License 2.0
* Documentation: https://kalasiris.readthedocs.io.


Features
--------

* Primarily a very lightweight wrapper around Python's subprocess module
* Calling compatibility with pysis_ (but not return types)
* Guaranteed to work with ISIS 3.6.0+, probably works with ISIS 3.0.0+
* Only guaranteed to work with Python 3.6.0+


ISIS
----

This library really only works if you already have ISIS_ installed and
working properly.


Quickstart
----------

Are you new to Python?  Or you just don't want to mess with
sophisticated Python installations?  Or you don't want to commit
to installing something when you don't know if it will be worth it?
Or you just want to write something 'real quick' in Python and just
need to call some ISIS programs **now**?

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
package that provide helper functions (like cubenormDialect) and
classes (like Histogram), and you don't get them by just grabbing
``kalasiris.py``.  Of course, you could get what you need out of
the ``kalasiris`` directory, but they may have more dependencies,
and at that point, you should probably look into just installing
kalasiris properly.


Installation
------------

*Eventually have some instructions here*


How is this different from pysis_?
----------------------------------

Folks got a lot of use out of pysis_, but it hasn't had a release
or commits in some time, and due to its implementation and strict
checking, it is not compatible with post 3.6.0 versions of ISIS.
The main kalasiris implementation can fit in one file and is very
lightweight.

Naturally, this means that working with kalasiris is perhaps less
forgiving, but we think it is more nimble.


-------

This repository layout was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _ISIS: https://isis.astrogeology.usgs.gov
.. _pysis: https://github.com/wtolson/pysis
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
