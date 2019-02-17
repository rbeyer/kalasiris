=====
Usage
=====

To use kalasiris in a project::

    import kalasiris


ISIS Interaction
----------------

When you import kalasiris, it looks for the ``ISISROOT`` and
``ISIS3DATA`` environment variables, so that it knows where to
find those programs on your system.

In the post ISIS 3.6.0 era, ISIS is installed via conda.  So you
have a base environment, and perhaps an isis3 environment.

You can probably install kalasiris in the isis3 environment via
any method of your choice, and then things will run as expected.

The trick is when you want to write a Python program that needs
a Python library that the isis3 conda environment doesn't support.

For example, you may want to write a Python program that uses
kalasiris and also the gdal_ library, so you might do this::

    % conda activate isis3
    (isis3) % conda install gdal
    Collecting package metadata: done
    ...
    The following packages will be REMOVED:

    isis3-3.6.0-py36_5
    ...


Whoa! What? The isis3 conda distribution needs to peg some
dependencies, so if you want to install gdal, it needs to uninstall
isis3 (detailed in `this ISIS issue
<https://github.com/USGS-Astrogeology/ISIS3/issues/615>`_).

So the solution is to install gdal (or whatever library you wanted
that caused this collision) in some other conda environment with
kalasiris, and run your Python there.  If you do that, you need a
way to tell kalasiris where the ISIS programs and data are.

Let's assume that you installed isis3, such that when you are in
your isis3 environment, these are the values of the ISIS environment
variables::

    ISISROOT=$HOME/anaconda3/envs/isis3
    ISIS3DATA=$HOME/anaconda3/envs/isis3/data

Where ``$HOME`` is your home directory.

You have at least two options:

1. Set it in your environment:
    When you activate your other conda environment (the one with
    gdal--or whatever--and kalasiris), just set those same variables
    in your environment, and kalasiris will see them when you import
    it in your Python code (even without having to run any kind of ISIS
    setup, just set the environment variables, but you could run the
    whole ISIS setup if you wanted to).

2. Set it in your Python program:
    You can add those paths to ``os.environ`` manually *before*
    you import kalasiris, like so:

::
   import os

   my_isisroot = os.path.join(os.eviron['HOME'],
                              'anaconda3','envs','isis3')
   os.environ['ISISROOT'] = my_isisroot
   os.environ['ISIS3DATA'] = os.path.join(my_isisroot, 'data')

   import kalasiris

Those environment variables were only set internally to the Python
runtime, not your actual shell, so they aren't there when the program
exits (unless you used ``putenv()`` to put them there), tidy!

Other possibilities exist, but either of these allows you to write Python
programs using kalasiris and run them from a conda environment (or anywhere)
that isn't the isis3 conda environment.

.. _gdal: https://gdal.org/
