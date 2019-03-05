.. highlight:: shell

============
Installation
============


Stable release
--------------

To install kalasiris, run this command in your terminal:

.. code-block:: console

    $ pip install kalasiris

This is the preferred method to install kalasiris, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

Alternately, you can install ``kalasiris`` from the `conda-forge`_ channel
by adding ``conda-forge`` to your channels with:

.. code-block:: console

    conda config --add channels conda-forge

Once the ``conda-forge`` channel has been enabled, ``kalasiris`` can be installed with:

.. code-block:: console

    conda install kalasiris

It is possible to list all of the versions of ``kalasiris`` available on your platform with:

.. code-block:: console

    conda search kalasiris --channel conda-forge


.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _conda-forge: https://anaconda.org/conda-forge/kalasiris


From sources
------------

The sources for kalasiris can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/rbeyer/kalasiris

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/rbeyer/kalasiris/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/rbeyer/kalasiris
.. _tarball: https://github.com/rbeyer/kalasiris/tarball/master
