#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Many ISIS programs require the creation of a fromlist file for input.
   These functions and classes provide convenient mechanisms for
   creating those files, or simply creating temporary versions.
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

import os
import tempfile
import sys
from pathlib import Path

# with fromlist.open([file1, file2, file3]) as fl:
#     isis.cubeit(fl, to='foo.cub')
#
# with fromlist.open([file1, file2, file3], pathlike='foo') as fl:
#     isis.cubeit(fl, to='foo.cub')
#
# fromlist_path = fromlist.make([file1, file2, file3])
# fromlist_path = fromlist.make([file1, file2, file3], pathlike='foo')


def print_fl(fromlist: list, file=sys.stdout):
    '''Works like 'print()', but when given a list, will write out
       that list, one element per line, and then will print a
       final empty line.

       This is the format that many ISIS programs which take a
       'FROMLIST=' parameter need.

       Therefore, if you wanted to create a fromlist file, you
       could do::

            with open('fromlist.txt', 'w') as f:
                fromlist.print_fl(['a.cub', 'b.cub', 'c.cub'], file=f)

            isis.cubeit(fromlist='fromlist.txt', to='stacked.cub')

       However, it is more likely that you would use 'fromlist.make()'
       or the 'fromlist.open_fl()' context manager.
    '''
    for elem in fromlist:
        print(str(elem), file=file)
    print('', file=file)


def make(fromlist: list, pathlike=None) -> Path:
    '''Creates a file with the fromlist elements one per line.

       If *pathlike* is given, that will be the path used, otherwise
       create a temporary file and return its path.

       You're responsible for deleting it after you're done.

       You can use it like this::

           fromlist_path = fromlist.make(['a.cub', 'b.cub', 'c.cub'])
           isis.cubeit(fromlist=fromlist_path, to='stacked.cub')
           fromlist_path.unlink()

       However, using the 'fromlist.open_fl()' context manager might
       be even more handy.
    '''
    filelike = None
    mode = 'wt'
    if pathlike is None:
        filelike = tempfile.NamedTemporaryFile(mode=mode, delete=False)
    else:
        filelike = open(pathlike, mode=mode)

    print_fl(fromlist, file=filelike)
    filelike.close()

    return Path(filelike.name)


class open_fl():
    '''This is a context manager that works similarly to open(), but
       for creating fromlist files.  Use it like this::

        with fromlist.open_fl(['a.cub', 'b.cub', 'c.cub']) as f:
            isis.cubeit(fromlist=f, to='stacked.cub')
    '''

    def __init__(self, fromlist: list, pathlike=None):
        self.fromlist = fromlist
        self.name = str(pathlike)
        self.temp = False
        self.file = None

        if pathlike is None:
            self.temp = True

    def __enter__(self):
        p = make(self.fromlist, self.name)
        self.file = open(p, mode='r')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        if self.temp:
            os.unlink(self.file.name)
