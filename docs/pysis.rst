=====
How is this different from pysis?
=====

Folks got a lot of use out of pysis_, but it hasn't had a release
or commits in some time, and due to its implementation and strict
checking, it is not compatible with post 3.6.0 versions of ISIS.
The main kalasiris implementation can fit in one file and is very
lightweight.

Naturally, this means that working with kalasiris is perhaps less
forgiving, but we think it is more nimble.

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

You now have to do this with kalasiris::

  k_value = kalasiris.getkey( from_='W1467351325_4.map.cal.cub',
                              keyword='minimumringradius',
                              grp='mapping').stdout

Note the ``.stdout`` at the end there to access the returned
``subprocess.CompletedProcess``'s ``.stdout`` attribute.

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

The one way that kalasiris is the same is that it supports the pysis
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



.. _pysis: https://github.com/wtolson/pysis
