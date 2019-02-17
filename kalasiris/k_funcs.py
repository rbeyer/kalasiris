#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides kalasiris _k functions.

   The kalasiris _k functions provide some syntactic sugar to make
   calling the ISIS programs just that much easier.  For example::

        import kalasiris as isis

        cube_file = 'some.cub'

        keyval = isis.getkey(cube_file, grpname='Instrument',
                         keyword='InstrumentId').stdout.strip()

        k_keyval = isis.getkey_k(cube_file, 'Instrument', 'InstrumentId')

   And the values of ``keyval`` and ``k_keyval`` are identical, its just
   that the _k function version is a little easier.  Each of the _k functions
   implements their modifications a little differently, so make sure to read
   their documentation.
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
import kalasiris as isis


def getkey_k(cube, group, key):
    '''Simplified calling for getkey.

    No default parameters are needed, and it directly returns a string.
    '''
    return(isis.getkey(cube, grpname=group, keyword=key).stdout.strip())


def hi2isis_k(img, **kwargs):
    '''Creates a default name for the to= cube.'''
    if 'to' not in kwargs:
        kwargs['to'] = os.path.splitext(img)[0] + '.cub'
    return(isis.hi2isis(img, **kwargs))
