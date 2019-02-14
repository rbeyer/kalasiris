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
    (isis3) & conda install gdal
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
    When you activate your your other conda environment (the one with
    gdal--or whatever--and kalasiris), just set those same variables
    in your environment, and kalasiris will see them when you import
    it in your Python code.

2. Set it in your Python program with the ``kalasiris.environ`` dictionary::

   import kalasiris

   my_isisroot = os.path.join(os.eviron['HOME'],'anaconda3','envs','isis3')
   my_isis3data = os.path.join( my_isisroot, 'data' )

   kalasiris.environ['ISISROOT'] = my_isisroot
   kalasiris.environ['ISIS3DATA'] = my_isis3data

Other possibilities exist, but either of these allows you to write Python
programs using kalasiris and run them from a conda environment (or anywhere)
that isn't the isis3 conda environment.

.. _pvl https://github.com/planetarypy/pvl
