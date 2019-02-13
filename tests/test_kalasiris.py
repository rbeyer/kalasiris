#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kalasiris` package."""

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
sys.path.append('../')
from kalasiris import *
#from kalasiris import kalasiris

img = 'HiRISE_test.img'

class TestParams(unittest.TestCase):
    def test_addparams(self):
        t = ( 'isisprogram','from=foo.cub' )
        p = { 'to': 'to.cub', 'check': False, 'value': 3.0 }
        c = list(t)
        truth = list(t)
        truth.extend( ['to=to.cub', 'check=False', 'value=3.0'] )

        c = addparams( c, p )
        self.assertEqual( truth, c )

class TestHistogram(unittest.TestCase):
    def setUp(self):
        self.cube = 'test_Histogram.cub'
        self.histfile = 'test_Histogram.hist'
        hi2isis(img, self.cube)
        hist(self.cube, to=self.histfile)

    def tearDown(self):
        os.remove('print.prt')
        os.remove(self.cube)
        os.remove(self.histfile)

    def test_init(self):
        h = Histogram( self.histfile )

    def test_dictlike(self):
        h = Histogram( self.histfile )
        self.assertEqual( self.cube, h['Cube'] )

    def test_listlike(self):
        h = Histogram( self.histfile )
        self.assertEqual( 5, len(h[0]) )

    def test_contains(self):
        h = Histogram( self.histfile )
        self.assertTrue( 'Std Deviation' in h )

    def test_len(self):
        h = Histogram( self.histfile )
        self.assertEqual( 107, len(h) )

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


# @unittest.skip('Takes a while to run hi2isis.')
class Test_hi2isis(unittest.TestCase):
    def setUp(self):
        self.img = img

    def tearDown(self):
        os.remove( 'print.prt' )

    def test_hi2isis_with_to(self):
        tocube = 'test_hi2isis.cub'
        hi2isis( self.img, tocube )
        self.assertTrue( os.path.isfile(tocube) )
        os.remove( tocube )

    def test_hi2isis_without_to(self):
        tocube = os.path.splitext( self.img )[0] + '.cub'
        hi2isis( self.img )
        self.assertTrue( os.path.isfile(tocube) )
        os.remove( tocube )

#@unittest.skip('Takes a while to run hi2isis.')
class Test_getkey(unittest.TestCase):
    def setUp(self):
        self.cub = 'test_getkey.cub'
        hi2isis( img, self.cub )

    def tearDown(self):
        os.remove( self.cub )
        os.remove( 'print.prt' )

    def test_getkey(self):
        truth = 'HIRISE'
        key = getkey( self.cub, 'Instrument', 'InstrumentId' )
        self.assertEqual( truth, key )

    def test_getkey_fail(self):
        # Pixels doesn't have InstrumentId, should fail
        self.assertRaises( subprocess.CalledProcessError, getkey, self.cub, 'Pixels', 'InstrumentId' )

#@unittest.skip('Takes a while to run hi2isis.')
class Test_histat(unittest.TestCase):
    def setUp(self):
        self.cub = 'test_histat.cub'
        hi2isis( img, self.cub )

    def tearDown(self):
        os.remove( self.cub )
        os.remove( 'print.prt' )

    def test_histat_with_to(self):
        tofile = self.cub+'.histat'
        histat( self.cub, to=tofile )
        self.assertTrue( os.path.isfile(tofile) )
        os.remove( tofile )

    def test_histat_without_to(self):
        s = histat( self.cub ).stdout
        self.assertTrue( s.startswith('Group = IMAGE_POSTRAMP') )


if __name__ == '__main__':
    if not os.path.isfile( img ):
        print( 'Downloading test HiRISE EDR image.' )
        urllib.request.urlretrieve( 'https://hirise-pds.lpl.arizona.edu/PDS/EDR/PSP/ORB_010500_010599/PSP_010502_2090/PSP_010502_2090_RED5_0.IMG', img )

    unittest.main()
