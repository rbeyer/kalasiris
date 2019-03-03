=====
Usage
=====

To use kalasiris in a project::

    import kalasiris


kalasiris Core
--------------

The central piece of the kalasiris library provides Python function calls
that allow you to easily run ISIS programs from within Python in a manner
similar to the way that you run ISIS programs on the command line.

So if you would type this in an ISIS enabled command line::

    (isis3) % catlab from=some.cub to=some.pvl

To achieve the same thing from within a Python program, you could do
this (you don't need to alias *kalasiris* as *isis* in your programs,
but it is shorter to type)::

    import kalasiris as isis

    isis.catlab('some.cub', to='some.pvl')

Of course, you could use variables instead of strings::

    import kalasiris as isis

    from_cube = 'some.cub'
    pvl_file = 'some.pvl'

    isis.catlab(from_cub, to=pvl_file)

Or with ``pathlib.Path`` objects::

    from pathlib import Path

    import kalasiris as isis

    from_path = Path('some.cub')

    isis.catlab(from_path, to=from_path.with_suffix('.pvl'))

Possibilities abound.

Each of the 300+ ISIS programs that you can use on the command line
can be called this way from within Python.

Most ISIS programs have a ``FROM=`` parameter, and so all kalasiris
versions of them will assume that the first item in the argument
signature is what should be assigned to the ``FROM=`` parameter if
you were typing the ISIS program at the command line, that's one
of the reasons why in the calls above you DO NOT write
``isis.catlab(from=from_cub, to=pvl_file)``.  The other reason is
that ``from`` is a reserved word in Python, so it just won't work.
If you really want to use a named parameter, you can append an
underbar to any parameter, like this::

    isis.catlab(from_=from_cub, to=pvl_file)

Or even like this::

    isis.catlab(from_=from_cub, to_=pvl_file)

There are some other reserved words like ``min``, so while you can't
have a ``min=something`` in your Python, you can do either of these::

    isis.hist('some.cub', min_=5)

    isis.hist('some.cub', minimum=5)

So trailing underbars can be handy.  In addition to the parameters
that each ISIS program has (like ``FROM=``, ``TO=``, etc.), ISIS
programs can also take what ISIS calls 'reserved parameters' which
are things like ``-restore=file`` or ``-log``. In order to use those
kinds of parameters from kalasiris, just append them with two
underbars (``_``) like so::

    isis.hist('some.cub', min_=5, gui__)

Which, when called in your Python program, would actually fire up
the GUI window for ISIS hist, with a default value for ``MINIMUM``
set to 5, where you could fiddle with controls, hit the run button,
and when you closed the window, your Python program would start
right back up where it left off.


kalasiris as wrapper
~~~~~~~~~~~~~~~~~~~~

We mention this from time to time, but what does it mean?  Well,
it means that whenever you call one of the 'ISIS' functions with
the kalasiris library, it basically just gathers the inputs, does
some stuff to build the right 'command line' and then passes that
to a call of Python's ``subprocess.run()`` function which takes care
of actually running the ISIS program.  Of course, what this means
is that you can also give a kalasiris ISIS program bad inputs, just
like you can on the command line::

    isis.spiceinit('some.cub', jesse='Awesome!')

which ``subprocess.call()`` would dutifully run ``spiceinit`` with.
Doing so would be the equivalent to typing this on the command line::

    (isis3) % spiceinit fr= some_file.cub jesse=awesome
    **USER ERROR** Invalid command line.
    **USER ERROR** Unknown parameter [jesse].

If you tried to do that in your Python, calling the above function
would throw a ``subprocess.CalledProcessError`` (because that's what
``subprocess.run()`` throws when something goes wrong).  And you
can either be prepared for that with a try-block, or the exception
will bubble up and halt your program, and you'll get errors that
you'll have to deal with.


What do kalasiris ISIS functions return?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the ISIS functions that kalasiris provides are wrappers around
a call to ``subprocess.run()``, every kalasiris ISIS function returns
a ``subprocess.CompletedProcess`` object.  Most of the time, you're
either going to want to ignore it, or get at the output of the ISIS
program, like so::

    import kalasiris as isis

    completed = isis.getkey('some.cub',
                            grp='Dimensions',
                            keyword='Samples')

    value = completed.stdout
    print(value)
    # prints '512' or whatever the string
    # is that's returned from getkey

    # you could also do it in one go:

    print(isis.getkey('some.cub',
                            grp='Dimensions',
                            keyword='Samples').stdout)

Of course, a  ``subprocess.CompletedProcess`` object has other
methods and attributes that you can use, if you need to.


ISIS Interaction
----------------

When you import kalasiris, it looks for the ``ISISROOT`` and
``ISIS3DATA`` environment variables, so that it knows where to
find those programs on your system.

In the post ISIS 3.6.0 era, ISIS is installed via conda.  So you
have a *base* environment, and perhaps an *isis3* environment.

You can probably install kalasiris in the *isis3* environment via
any method of your choice, and then things will run as expected.

The trick is when you want to write a Python program that needs
a Python library that the isis3 conda environment doesn't support.

For example, you may want to write a Python program that uses
kalasiris and also the GDAL_ library, so you might do this::

    % conda activate isis3
    (isis3) % conda install gdal
    Collecting package metadata: done
    ...
    The following packages will be REMOVED:

    isis3-3.6.0-py36_5
    ...


Whoa! What? The isis3 conda distribution needs to peg some
dependencies, so if you want to install GDAL, it needs to uninstall
isis3 (detailed in `this ISIS issue
<https://github.com/USGS-Astrogeology/ISIS3/issues/615>`_).

So the solution is to install GDAL (or whatever library you wanted
that caused this collision) in some other conda environment with
kalasiris, and run your Python there.  If you do that, you need a
way to tell kalasiris where the ISIS programs and data are.

Let's assume that you installed isis3, such that when you are in
your *isis3* environment, these are the values of the ISIS environment
variables::

    ISISROOT=$HOME/anaconda3/envs/isis3
    ISIS3DATA=$HOME/anaconda3/envs/isis3/data

Where ``$HOME`` is your home directory.

You have at least two options:

1. Set it in your environment:
    When you activate your other conda environment (the one with
    GDAL--or whatever--and kalasiris), just set those same variables
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
that isn't the *isis3* conda environment.

.. _gdal: https://gdal.org/
