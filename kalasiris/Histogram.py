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

import collections, csv

class Histogram:
    """A class to read and wrap the contents of the output of the ISIS hist program, kalasiris.hist()"""

    def __init__(self, histfile):
        self.histfile = histfile
        (self.dictionary,
         self.headers,
         self.hist_list) = self.parsehist(histfile)
         # self.hist_list is a list of collections.namedtuple( 'HistRow', self.headers )

    def __str__(self):
        pass

    def __repr__(self):
        return (f'{self.__class__.__name__}(\'{self.histfile}\')')

    def __len__(self):
        return len(self.hist_list)

    def __getitem__(self,key):
        #if key is integer or slice object, look in self.hist_vals
        if isinstance(key, int):
            return self.hist_list[key]

        elif isinstance(key, slice):
            return self.hist_list[key]

        elif isinstance(key, str):
            return self.dictionary[key]

    def __iter__(self):
        return self.hist_list.__iter__()

    def __contains__(self, item):
        if item in self.dictionary: return True
        else: return False

    def keys(self):
        return self.dictionary.keys()

    def values(self):
        return self.dictionary.values()

    def parsehist(self, histfile):
        d = dict()
        headers = []
        hist_vals= []
        with open( histfile ) as f:
            for line in f:
                if ':' in line:
                    (k,v) = line.split(':')
                    if 'Cube' in k: d[k.strip()] = v.strip()
                    else:           d[k.strip()] = float(v.strip())

                if line.startswith('DN,'):
                    headers = line.strip().split(',')
                    HistRow = collections.namedtuple( 'HistRow', headers )
                    for row in map( HistRow._make, csv.reader(f, quoting=csv.QUOTE_NONNUMERIC) ):
                        hist_vals.append( row )

        return d, headers, hist_vals
