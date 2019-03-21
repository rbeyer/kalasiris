#!/usr/bin/env python
"""This module contains the PathSet Class.

   Working with ISIS can result in a lot of files to keep track of.
   The PathSet Class is simply a mutable set that only takes Path
   objects.  If you need to keep track of a bunch of files (typically
   to delete them after a set of processing calls), you can use a
   PathSet to keep track of them, and then delete them, like so::

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

# Copyright 2019, Ross A. Beyer (rbeyer@seti.org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path


class PathSet(set):
    """A class for containing a set of Path objects."""

    def __init__(self, iterable=None):
        if iterable:
            for value in iterable:
                if not isinstance(value, Path):
                    raise TypeError('only accepts pathlib.Path objects')
            super().__init__(iterable)
        else:
            super().__init__()

    def add(self, elem):
        '''This variation on add() returns the element.'''
        if not isinstance(elem, Path):
            raise TypeError('only accepts pathlib.Path objects')
        super().add(elem)
        return elem

    def unlink(self):
        '''Just runs Path.unlink() on all members.'''
        for p in self:
            p.unlink()
