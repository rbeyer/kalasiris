===================
kalasiris and pysis
===================

The kalasiris module mostly provides the same functionality as
pysis_, namely the easy ability to call ISIS programs from Python.
Of course, there are some differences, and some similarities.


How is this different from pysis_?
----------------------------------

Folks get a lot of use out of pysis_, but its implementation is a
'thick' wrapper around calls to ISIS programs, and has an architecture
which is complex.

We wrote kalasiris to provide a much lighter architecture around
calls to ISIS programs.  The main kalasiris implementation (what
we call the kalasiris core) can fit in one Python file (of about
150 lines, half of which are comments and documentation) and is
very programmatically simple.  This makes it easy to build more
complicated structures on top of.

There is also some compatibility with pysis_ calling syntax, and a
way to 'emulate' pysis with kalasiris for older code you might have.


Differences
-----------

What is returned from calls to ISIS programs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pysis_ library wrapped the call to subprocess tightly and just
returned ``stdout`` from the process as a byte string.  Whereas
kalasiris returns a ``subprocess.CompletedProcess`` object that you
can do more with.

So while you could do this in pysis::

  p_value = pysis.getkey( from_='W1467351325_4.map.cal.cub',
                          keyword='minimumringradius',
                          grp='mapping')

To get the same thing, you would do this with kalasiris::

  k_value = kalasiris.getkey( from_='W1467351325_4.map.cal.cub',
                              keyword='minimumringradius',
                              grp='mapping').stdout

Note the ``.stdout`` at the end there to access the returned
subprocess.CompletedProcess's stdout attribute.

Actually, the ``p_value`` is a byte string, while ``k_value``
is a string.  Odds are good you want a regular string anyway, but
if you really wanted complete parity, such that ``k_value`` would
be the same type as ``p_value`` was, you can do this::

    k_value = kalasiris.getkey( from_='W1467351325_4.map.cal.cub',
                                keyword='minimumringradius',
                                grp='mapping').stdout.encode()



No IsisPool
~~~~~~~~~~~

The pysis_ library provided multiprocessing support, but the
modern form of Python has a variety of good builtin modules
for concurrent execution that provide more features, and we
didn't feel that we could do better.


Compatibility
-------------

The one way that kalasiris is the same is that it supports the pysis_
syntax to protect Python reserved words like ``from`` and ``min``,
by appending an underbar (``_``) to the parameter name.  This allows
the user to provide 'natural' function calls like::

    cubefile = 'some.cub'
    kalasiris.stats(from_=cubefile)

Since almost all of the ISIS programs have a ``from=`` parameter, kalasiris
also supports the syntax that allows one non-default parameter value, and assumes
that it is what should be given to the ISIS program's ``from=`` parameter, so
the above could also be written::

    kalasiris.stats(cubefile)

If you have some code that was written with pysis_ that you would
like to slowly switch over to kalasiris, but just changing ``from
pysis import isis`` to ``import kalasiris as isis`` resulted in a
bunch of errors, then we have a crutch for you.  The kalasiris
library has a pysis emulation module that emulates pysis return
types and exceptions.  To give this a try, replace your ``from pysis
import isis`` to ``import kalasiris.pysis as isis`` and see if that
works for you.  This emulation is new, so may be buggy.


Which to use?
-------------

Given all this, which should you use?  We can't really answer that
in an unbiased way, so you probably should get a second opinion,
but here goes:

If you are already using pysis_ and your software is working, don't
switch.

If you are programming exclusively in Python 2, use pysis_ because
kalasiris won't work under Python 2 (but really, start using Python
3).

If you are programming in Python 3, starting a new project, and
you are trying to decide between pysis_ and kalasiris, give kalasiris
a try.

If there are some tricky things that you want to do that pysis_ doesn't
quite support then maybe look into kalasiris, as our architecture might be
more flexible for you.


.. _pysis: https://github.com/wtolson/pysis
