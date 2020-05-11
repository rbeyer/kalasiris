#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Many ISIS programs require the creation of a fromlist file for input.
These functions and classes provide convenient mechanisms for
creating those files, or simply creating temporary versions.
"""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import builtins
import os
import tempfile
import sys
import warnings
from pathlib import Path

# with fromlist.open([file1, file2, file3]) as fl:
#     isis.cubeit(fl, to='foo.cub')
#
# with fromlist.open([file1, file2, file3], pathlike='foo') as fl:
#     isis.cubeit(fl, to='foo.cub')
#
# fromlist_path = fromlist.make([file1, file2, file3])
# fromlist_path = fromlist.make([file1, file2, file3], pathlike='foo')


def print(fromlist: list, file=sys.stdout):
    """Works like :func:`print`, but when given a list, will write out
    that list, one element per line.

    This is the format that many ISIS programs which take a
    ``FROMLIST=`` parameter need.

    Therefore, if you wanted to create a fromlist file, you
    could do::

         with open('fromlist.txt', 'w') as f:
             fromlist.print(['a.cub', 'b.cub', 'c.cub'], file=f)

         isis.cubeit(fromlist='fromlist.txt', to='stacked.cub')

    However, it is more likely that you would use :func:`.fromlist.make()`
    or the :class:`.fromlist.temp()` context manager.
    """
    for elem in fromlist:
        builtins.print(str(elem), file=file)


def print_fl(fromlist: list, file=sys.stdout):
    """Synonym for :func:`.fromlist.print()`

    *This function is deprecated, and may be removed
    at the next major patch.*
    """
    warnings.warn(
        "Original syntax, may be removed at next major patch. "
        "Use fromlist.print() instead.",
        DeprecationWarning,
    )
    print(fromlist, file)


def make(fromlist: list, pathlike=None) -> Path:
    """Creates a file with the fromlist elements one per line.

    If *pathlike* is given, that will be the path used, otherwise
    create a temporary file and return its path.

    You're responsible for deleting it after you're done.

    You can use it like this::

        fromlist_path = fromlist.make(['a.cub', 'b.cub', 'c.cub'])
        isis.cubeit(fromlist=fromlist_path, to='stacked.cub')
        fromlist_path.unlink()

    However, using the :class:`.fromlist.temp()` context manager might
    be even more handy.
    """
    mode = "wt"
    if pathlike is None:
        filelike = tempfile.NamedTemporaryFile(mode=mode, delete=False)
    else:
        filelike = open(pathlike, mode=mode)

    print(fromlist, file=filelike)
    filelike.close()

    return Path(filelike.name)


class open_fl:
    """This is a context manager that works similarly to :func:`open`, but
    for creating fromlist files.  Use it like this::

     with fromlist.open_fl(['a.cub', 'b.cub', 'c.cub']) as f:
         isis.cubeit(fromlist=f.name, to='stacked.cub')

    Its probably better to use :class:`.fromlist.temp()`, however.

    *This context manager is deprecated, and may be removed
    at the next major patch.*
    """

    warnings.warn(
        "Original syntax, may be removed at next major patch. "
        "Use fromlist.temp() instead.",
        DeprecationWarning,
    )

    def __init__(self, fromlist: list, pathlike=None):
        self.fromlist = fromlist
        self.name = str(pathlike)
        self.temp = False
        self.file = None

        if pathlike is None:
            self.temp = True

    def __enter__(self):
        p = make(self.fromlist, self.name)
        self.file = open(p, mode="r")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        if self.temp:
            os.unlink(self.file.name)


class temp:
    """This is a context manager that creates a temporary
    fromlist file and then gets rid of it for you.
    Use it like this::

     with fromlist.temp(['a.cub', 'b.cub', 'c.cub']) as f:
         isis.cubeit(fromlist=f, to='stacked.cub')

    The object that is bound to the *as* clause of the with
    statement is a :class:`pathlib.Path()`.
    """

    def __init__(self, fromlist: list):
        self.path = make(fromlist)

    def __enter__(self) -> Path:
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.path.unlink()
