#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The ISIS cubenorm file outputs plain text table information and
   also reads it in, but the format is a very specific fixed-width
   table format.  A plain csv.reader or csv.DictReader using the
   cubenormfile.Dialect object will be able to read the text output
   of cubenorm, but to write out a file that cubenorm will read in,
   you will need to use the cubenormfile.writer or
   cubenormfile.DictWriter classes.
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

import csv

# Establish the allowable cubenorm fieldnames and their character widths.
fieldnames = ('Band', 'RowCol', 'ValidPoints', 'Average',
              'Median', 'StdDev', 'Minimum', 'Maximum')

# These widths are extremely fragile, and if cubenorm changes,
# then these will need to be changed, too.
fieldwidth = dict()
for n in fieldnames:
    fieldwidth.setdefault(n, 15)
fieldwidth['Band'] = 8
fieldwidth['RowCol'] = 8


class Dialect(csv.Dialect):
    '''A csv.Dialect for the output of the ISIS cubenorm program.'''
    delimiter = ' '
    skipinitialspace = True
    quoting = csv.QUOTE_NONE
    escapechar = ''
    lineterminator = '\n'


class writer:
    '''A class for writing out the fixed-width format required by cubenorm.

    The interface is similar to the csv.writer class, but does not inheirit
    from it.'''

    def __init__(self, f):
        self.file_object = f

    def writerow(self, row):
        line = ''
        for name, elem in zip(fieldnames, row):
            right_aligned = '{:>' + str(fieldwidth[name]) + '}'
            line += right_aligned.format(elem)

        self.file_object.write(line + '\n')

    def writerows(self, rows):
        for r in rows:
            self.writerow(r)

    def writeheader(self):
        '''A convenence function, since the fieldnames are pre-defined.'''
        self.writerow(fieldnames)


class DictWriter(csv.DictWriter):
    '''A DictWriter for cubenorm files.'''

    def __init__(self, f, restval="", extrasaction="raise",
                 dialect=Dialect, *args, **kwds):
        self.fieldnames = fieldnames
        self.restval = restval
        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError("extrasaction (%s) must be 'raise' or 'ignore'"
                             % extrasaction)
        self.extrasaction = extrasaction
        self.writer = writer(f)
