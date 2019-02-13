#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `cubenormDialect` class."""

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


import unittest

import os, sys, unittest
import shutil, urllib.request
#sys.path.append('../')
from kalasiris import *
#from kalasiris import kalasiris

img = 'HiRISE_test.img'

class TestCubenormDialect(unittest.TestCase):
    def setUp(self):
        self.cube = 'test_cubenorm.cub'
        self.statsfile = 'test_cubenorm.stats'
        hi2isis(img, self.cube)
        cubenorm( self.cube, stats=self.statsfile )

    def tearDown(self):
        os.remove('print.prt')
        os.remove(self.cube)
        os.remove(self.statsfile)

    def test_cubenorm_reader(self):
        with open( self.statsfile ) as csvfile:
            reader = csv.reader( csvfile, dialect=cubenormDialect )
            for row in reader:
                self.assertEqual( 8, len(row) )
                break


if __name__ == '__main__':
    if not os.path.isfile( img ):
        print( 'Downloading test HiRISE EDR image.' )
        urllib.request.urlretrieve( 'https://hirise-pds.lpl.arizona.edu/PDS/EDR/PSP/ORB_010500_010599/PSP_010502_2090/PSP_010502_2090_RED5_0.IMG', img )

    unittest.main()
