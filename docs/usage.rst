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

    (isis) % catlab from=some.cub to=some.pvl

To achieve the same thing from within a Python program, you could do
this (you don't need to alias *kalasiris* as *isis* in your programs,
but it is shorter to type)::

    import kalasiris as isis

    isis.catlab('some.cub', to='some.pvl')

Of course, you could use variables instead of strings::

    import kalasiris as isis

    from_cube = 'some.cub'
    pvl_file = 'some.pvl'

    isis.catlab(from_cube, to=pvl_file)

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
of the reasons why the above examples aren't written like ``isis.catlab(from=from_cub,
to=pvl_file)`` but they could be.  If you do this, your syntax-aware
editor might highlight or complain that ``from`` is a reserved word
in Python, and you think maybe it shouldn't be used as a named
argument like this.  Your editor might be concerned, but Python
isn't.  However, if you don't like the look of this, you can append
an underbar to any parameter, like this::

    isis.catlab(from_=from_cub, to=pvl_file)

Or even like this::

    isis.catlab(from_=from_cub, to_=pvl_file)

There are some other reserved words like ``min``, that your editor
might also not like, so if you don't want to have a ``min=something``
in your Python, you can do either of these::

    isis.hist('some.cub', min_=5)

    isis.hist('some.cub', minimum=5)

Trailing underbars can be handy.  In addition to the parameters
that each ISIS program has (like ``FROM=``, ``TO=``, etc.), ISIS
programs can also take what ISIS calls 'reserved parameters' which
are things like ``-restore=file`` or ``-log``. In order to use those
kinds of parameters from kalasiris, either add them with their leading
dash or with two underbars (``_``) as string parameters, the following two lines are
identical::

    isis.hist('some.cub', "gui__", min_=5)
    isis.hist('some.cub', "-gui", min_=5)

Which, when called in your Python program, would actually fire up
the GUI window for ISIS hist, with a default value for ``MINIMUM``
set to 5, where you could fiddle with controls, hit the run button,
and when you closed the window, your Python program would start
right back up where it left off.

The reserved parmeters that take an argument must use the form with
trailing underbars since those are passed as keys with Python variable names, like so::

    isis.spiceinit('some.cub', restore__=Path("to/some/file"))


If you are a user of preference files with ISIS, you might find yourself constantly
passing the `pref__` parameter to all of your kalasiris calls in a program file.  As
a convenience, we provide `kalasiris.set_persistent_preferences()` so that you can
set this once, and the "-pref" argument with that path will be added to every
kalasiris call you make.

Logging
~~~~~~~

The kalasiris library uses the Logging Facility API provided by the
Python standard library.  When you run any of the ISIS "functions"
with kalasiris, what would be entered on the command line (the ISIS
program name, the arguments, etc.) are logged with a log level of
INFO.

So if you wanted to have your program write out information about
the ISIS programs that are being called, you just need to set up a
basic logger in your program like so::

    import logging
    import kalasiris as isis
    logging.basicConfig(level=logging.INFO)
    isis.spiceinit("my.cub")

Then on stderr, you'd get this message::

    spiceinit from=my.cub

Without importing the logging module and calling the basicConfig
method, nothing would be printed to stderr, but my.cub would
still be spiceinit'ed.  This logging functionality is meant to stay
out of your way when you don't want it, but easier to use than
having to format this yourself every time you want to see what's going on.

Maybe by default, you'd set your logger to only log at logging.WARNING,
but if someone gave your program the -v flag or something, you'd set it
to logging.INFO so they could see everything.


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

    (isis) % spiceinit fr= some_file.cub jesse=awesome
    **USER ERROR** Invalid command line.
    **USER ERROR** Unknown parameter [jesse].

If you tried to do that in your Python, calling the above function
would throw a ``subprocess.CalledProcessError`` (because that's what
``subprocess.run()`` throws when something goes wrong).  And you
can either be prepared for that with a try-block, or the exception
will bubble up and halt your program, and you'll get errors that
you'll have to deal with.

If you have a program that is using a lot of kalasiris calls, you might
want to consider running them wrapped in a try-block that looks like this::

    try:
        # various kalasiris calls or calls to functions which
        # use kalasiris.

    except subprocess.CalledProcessError as err:
        print('Had an ISIS error:')
        print(' '.join(err.cmd))
        print(err.stdout)
        print(err.stderr)
        raise err

If you don't catch the ``subprocess.CalledProcessError`` like this
and print out all of its elements, you won't have good visibility
into the problem that ISIS had.  You'll see the error Python had
("this subprocess failed") but not the error ISIS had ("this ISIS
program failed in this way").  The other advantage is that this
also prints out the actual command that was given to ISIS, so you
can copy this from the printed error message and paste it to your
own command line to run directly, which can help diagnose the
problem.

Finally, the Python subprocess.run() command also has arguments that
you might want to take advantage of, and you can do so by passing arguments
to your kalasiris ISIS function with "leading" underbars, like so::

    import kalasiris as isis
    working_dir = Path("to/some/other/directory")
    edr = Path("/some/hirise.IMG")
    cube = Path("/output/hirise.cub")
    isis.hi2isis(edr, to=cube, _cwd=working_dir)

In this case, the first argument is used as 'FROM=' for ISIS, and the ``cube``
variable is the 'TO=" parameter for hi2isis, but the ``_cwd`` is stripped out
and its value (``working_dir``) is given to the ``subprocess.run()``
as the ``cwd`` argument.  This means that ``subprocess.run()`` will change to
that directory and run there, (so you'll probably end up with a ``print.prt``
file there.  That may not seem very important, and it is unlikely you will
need this often, but if you are trying to run some ISIS programs in parallel,
and they all need to write to the same file, then being able to create a
set of different working directories and having them each rooted in their own,
so they don't clash, can be helpful.  Surely, there are lots of other handy
uses for arguments to ``subprocess.run()``, and you have access to all of them.



What do kalasiris ISIS functions return?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the ISIS functions that kalasiris provides are wrappers around
a call to ``subprocess.run()``, every kalasiris ISIS function returns
a ``subprocess.CompletedProcess`` Python Standard Library object.
Most of the time, you're either going to want to ignore it, or get
at the output of the ISIS program, like so::

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
``ISISDATA`` (also accepts ``ISIS3DATA``) environment variables,
so that it knows where to find those programs and resources on your system.

In the post ISIS 3.6.0 era, ISIS is installed via conda.  So you
have a *base* environment, and perhaps an *isis* environment.

You can probably install kalasiris in the *isis* environment via
any method of your choice, and then things will run as expected.

The trick is when you want to write a Python program that needs
a Python library that the isis conda environment doesn't support.

For example, you may want to write a Python program that uses
kalasiris and also the GDAL_ library, so you might do this::

    % conda activate isis
    (isis) % conda install gdal
    Collecting package metadata: done
    ...
    The following packages will be REMOVED:

    isis3-3.6.0-py36_5
    ...


Whoa! What? The isis conda distribution needs to peg some
dependencies, so if you want to install GDAL, it needs to uninstall
isis (detailed in `this ISIS issue
<https://github.com/USGS-Astrogeology/ISIS3/issues/615>`_).

So the solution is to install GDAL (or whatever library you wanted
that caused this collision) in some other conda environment with
kalasiris, and run your Python there.  If you do that, you need a
way to tell kalasiris where the ISIS programs and data are.

Let's assume that you installed isis, such that when you are in
your *isis* environment, these are the values of the ISIS environment
variables::

    ISISROOT=$HOME/anaconda3/envs/isis
    ISISDATA=$HOME/anaconda3/envs/isis/data

Where ``$HOME`` is your home directory.

You have at least three options:

1. Use conda stacking:
    First ``conda activate isis`` and then ``conda activate --stack other-env``
    which enables these enviroments like nested dolls, so that you'll end up
    in a situation with the ISIS environment variables set correctly for
    kalasiris to find, and your other-env with kalasiris and whatever else
    you need.

2. Set it in your environment manually:
    When you activate your other conda environment (the one with
    GDAL--or whatever--and kalasiris), just set those same variables
    in your environment, and kalasiris will see them when you import
    it in your Python code (even without having to run any kind of ISIS
    setup, just set the environment variables, but you could run the
    whole ISIS setup if you wanted to, or get fancy and install activate.d
    and deactivate.d scripts in your other environment).

3. Set it in your Python program:
    You can add those paths to ``os.environ`` manually *before* you
    import kalasiris, like so (your argument to ``os.path.join``
    may vary depending on where your isis conda environment is)::

        import os

        my_isisroot = os.path.join(os.eviron['HOME'],
                                   'anaconda3','envs','isis')
        os.environ['ISISROOT'] = my_isisroot
        os.environ['ISISDATA'] = os.path.join(my_isisroot, 'data')

        import kalasiris

Those environment variables were only set internally to the Python
runtime, not your actual shell, so they aren't there when the program
exits.

Other possibilities certainly exist, but these allow you to write Python
programs using kalasiris and run them from a conda environment (or anywhere)
that isn't the *isis* conda environment.

.. _gdal: https://gdal.org/
