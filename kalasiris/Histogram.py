#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import collections
import csv
import itertools
import os
from .k_funcs import hist_k


class Histogram(collections.abc.Sequence):
    """Reads the output from ISIS hist and provides it as a sequence.

       The resulting Histogram object primarily behaves like a list, where
       that list represents the rows of the ISIS hist output.  Each of those
       rows is a ``namedtuple`` which contains the elements of each row,
       referenced by their column names.

       The Histogram object also has some dictionary-like capabilities, in
       order to get at the values listed in the ISIS hist output in the
       section before the numerical output.
    """

    def __init__(self, histinfo):
        self.histinfo = histinfo

        # if isinstance(histinfo, os.PathLike):
        if os.path.isfile(histinfo):
            with open(histinfo) as f:
                iscube = f.readline().split(':')[0]

            if 'Cube' == iscube:
                with open(histinfo, 'r') as f:
                    contents = f.read()

                (self.dictionary, self.headers, self.hist_list) \
                    = self.parse(contents)
            else:
                (self.dictionary, self.headers, self.hist_list) \
                    = self.parse(hist_k(histinfo))

            # (self.dictionary, self.headers, self.hist_list) \
            #     = self.parsehistfile(histinfo)
        else:
            (self.dictionary, self.headers, self.hist_list) \
                = self.parse(histinfo)

        # self.hist_list is a list of
        # collections.namedtuple( 'HistRow', self.headers )

    def __str__(self):
        return(str(self.dictionary))

    def __repr__(self):
        return (f'{self.__class__.__name__}(\'{self.histfile}\')')

    def __len__(self):
        return len(self.hist_list)

    def __getitem__(self, key):
        # if key is integer or slice object, look in self.hist_list
        if isinstance(key, int):
            return self.hist_list[key]

        elif isinstance(key, slice):
            return self.hist_list[key]

        elif isinstance(key, str):
            return self.dictionary[key]

    def __iter__(self):
        return self.hist_list.__iter__()

    def __contains__(self, item):
        if item in self.dictionary:
            return True
        elif item in self.hist_list:
            return True
        else:
            return False

    def keys(self):
        '''Gets the keys from the initial portion of the hist output file.

           These will be items like 'Cube', 'Band', 'Average', etc.
        '''
        return self.dictionary.keys()

    def values(self):
        '''Gets the values from the initial portion of the hist output file.'''
        return self.dictionary.values()

    @staticmethod
    def parse(histinfo: str) -> tuple:
        '''Takes a string (expecting the output of ISIS ``hist``), and
           parses the output.

           A three-element namedtuple is returned: the first element is a *dictionary*
           of the name:value information at the top of the file, the second
           element is a *list* of the of the fields that decorate the top of the
           histogram rows, and the third element is a *list* of HistRow namedtuples
           that represent each row of the hist output.

           The contents of the file that results from ISIS ``hist`` look like
           this::

            Cube:           PSP_010502_2090_RED5_0.EDR_Stats.cub
            Band:           1
            Average:        6490.68
            [... other lines like this ...]
            His Pixels:      0
            Hrs Pixels:      0


            DN,Pixels,CumulativePixels,Percent,CumulativePercent
            3889,1,1,4.88281e-05,4.88281e-05
            3924,1,2,4.88281e-05,9.76563e-05
            3960,2,4,9.76563e-05,0.000195313
            [... more comma-separated lines like above ...]

           But this function sees it like this::

            k: v
            k: v
            k: v
            [... other lines like this ...]
            k: v
            k: v


            h,h,h,h,h
            n,n,n,n,n
            n,n,n,n,n
            n,n,n,n,n
            [... more comma-separated lines like above ...]

           First, it takes all of the ``k``s and ``v``s and saves them as the
           keys and values in the returned Histogram's dictionary.

           It takes the ``h``s and uses them as the set of fieldnames in the
           Histogram.

           It takes all of the lines with ``n``s and stores them as
           ``namedtuples`` in the Histogram's primary list.

        '''
        d = dict()
        fieldnames = []
        hist_rows = []
        for line in filter(lambda x: ':' in x, histinfo.splitlines()):
            (k, v) = line.split(':')
            if 'Cube' in k:
                d[k.strip()] = v.strip()
            else:
                d[k.strip()] = float(v.strip())

        reader = csv.reader(filter(lambda x: ',' in x, histinfo.splitlines()))
        fieldnames = next(reader)

        HistRow = collections.namedtuple('HistRow', fieldnames)
        for row in map(HistRow._make, reader):
            hist_rows.append(row)

        # Why not just return a Histogram here?:
        HistParsed = collections.namedtuple('HistParsed', ['info',
                                            'fieldnames', 'data'])
        return(HistParsed(d, fieldnames, hist_rows))
