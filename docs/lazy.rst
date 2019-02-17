============
Lazy Loading
============

The current implementation of kalasiris uses a Factory Pattern to build
a function for each ISIS program that it finds on the system.

You might consider that inelegant, as it will build a function for
each of the 300+ ISIS programs, even if you only use one.  The
``kalasiris.py`` and ``__init__.py`` files can be modified to not build
this long list of functions, but to only lazy-load the right function
when it is asked for.  The test implementation described below
describes that, but it isn't particularly faster nor does it use
less resources (and it makes the code harder to read).

Perhaps this is because there is extra overhead involved to instantiate
a class, and leverage its exception mechanism when an attribute
call tries to call a function that doesn't exist. Then it runs
the Factory to build it on demand.  We also then need to use
``sys.module`` calls to bootstrap the namespace correctly up to the
top level.


Gedanken Implementation
-----------------------

Well, it isn't really a 'thought implementation,' a test implementation
was built and lightly tested.

Make a ``kalasirisModule(types.ModuleType)`` class that encapsulates
all of the loose functions in ``kalasiris.py``.  And delete the ``for
p in _get_isis_program_names()`` loop.

The functions all need to have their signatures modified to take
``self``, but you should probably ``@staticmethod param_fmt()``.  Remove
the ``setattr()`` call and have ``_build_isis_fn()`` return the built
``isis_fn()``.  Optionally experiment with leaving it in, so that
once the factory is triggered to build a function, it stays in the
module.  Otherwise every time an ISIS function is called , the
Factory would have to build it again.

Then build a function that looks like this::

    def __getattr__(self, name):
        print('Got to overridden __getattr__ !')
        if name in self._get_isis_program_names():
            # remember to rewrite _build_isis_fn() to return its isis_fn()
            return(self._build_isis_fn(name))
        else:
            raise AttributeError

This is part of the the magic.  The ``kalasirisModule`` class's
``__getattr__()`` gets called when something tries to access an
attribute that doesn't exist on the class.  This then runs the
Factory to make the ISIS function on the spot.

Finally after you close the class, add this line::

  sys.modules[__name__] = kalaModule(__name__)

This pattern is a sanctioned hack of the import system.  This
sys.modules[] assignment within ``kalasiris.py`` basically replaces
the namespace of the file with the namespce of the ``kalasirisModule()``
class, which enables it to receive the call to ``__getattr__()`` if
it were loaded directly.

Of course, given our structure, we want to leverage ``__init__.py``
to load ``kalasiris.py`` and the other files to present a unified
whole when someone loads the whole package.

To do that, we need to use the ``sys.modules[]`` hack to bootstrap
the namespace up another level.

So in in __init__.py, add this at the very top::

  from sys import modules

And then this after the ``from ... import`` statements::

  modules[__name__] = kalasiris

  setattr(modules[__name__], 'Histogram', Histogram)
  setattr(modules[__name__], 'cubenormDialect', cubenormDialect)

Setting ``modules[__name__]`` brings up the namespace up a level, but
then masks the imports of Histogram and cubenormDialect from being
exposed, so you need to setattr them to add them back to the namespace
that is exposed when someone loads the package.  Clearly, something
more elegant than a bunch of individual ``setattr()`` calls, but this
gets the point across.
