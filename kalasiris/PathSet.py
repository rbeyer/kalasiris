#!/usr/bin/env python
"""This module contains the PathSet Class.

orking with ISIS can result in a lot of files to keep track of.
he PathSet Class is simply a mutable set that only takes
class:`pathlib.Path` objects.  If you need to keep track of a
unch of files (typically to delete them after a set of processing
alls), you can use a :class:`.PathSet` to keep track of them, and then
elete them, like so::

    import kalasiris as isis

    to_delete = isis.PathSet()

    input_p = Path('some.fits')
    output_p = input_p.with_suffix('.done.cub')

    isis_cub = to_delete.add(input_p.with_suffix('.cub'))
    isis.lorri2isis(input_fits, to= isis_cub)

    first = to_delete.add(input_p..with_suffix('.1.cub'))
    isis.some_progeram(isis_cub, to=first)

    second = to_delete.add(input_p..with_suffix('.2.cub'))
    isis.some_program(first, to=second)

    isis.final_step(second, to=output_p)

    to_delete.unlink()
"""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

from pathlib import Path


class PathSet(set):
    """A class for containing a set of :class:`pathlib.Path` objects."""

    def __init__(self, iterable=None):
        if iterable:
            for value in iterable:
                if not isinstance(value, Path):
                    raise TypeError("only accepts pathlib.Path objects")
            super().__init__(iterable)
        else:
            super().__init__()

    def add(self, elem) -> Path:
        """This variation on add() returns the element."""
        if not isinstance(elem, Path):
            raise TypeError("only accepts pathlib.Path objects")
        if elem in self:
            raise ValueError(
                f"The {elem} object is already a member of the PathSet."
            )
        super().add(elem)
        return elem

    def unlink(self):
        """Just runs Path.unlink() on all members."""
        for p in self:
            p.unlink()
