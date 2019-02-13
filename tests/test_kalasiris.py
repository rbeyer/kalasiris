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

import os, subprocess, unittest
import kalasiris as isis

# Hardcoding this, but I sure would like a better solution.
# One could download the .img file from the PDS at each setUp,
# but that seems like a lot of network traffic, when you could just
# do it once.
img = 'tests/resources/HiRISE_test.img'

class TestParams(unittest.TestCase):
    def test_param_fmt(self):
        t = ( 'isisprogram','from=foo.cub' )
        p = { 'to': 'to.cub', 'check': False, 'value': 3.0 }
        cmd = list(t)
        truth = list(t)
        truth.extend( ['to=to.cub', 'check=False', 'value=3.0'] )

        cmd.extend( map(isis.param_fmt, p.keys(), p.values()) )
        self.assertEqual( truth, cmd )


# @unittest.skip('Takes a while to run hi2isis.')
class Test_hi2isis(unittest.TestCase):
    def setUp(self):
        self.img = img

    def tearDown(self):
        os.remove( 'print.prt' )

    def test_hi2isis_with_to(self):
        tocube = 'test_hi2isis.cub'
        isis.hi2isis( self.img, tocube )
        self.assertTrue( os.path.isfile(tocube) )
        os.remove( tocube )

    def test_hi2isis_without_to(self):
        tocube = os.path.splitext( self.img )[0] + '.cub'
        isis.hi2isis( self.img )
        self.assertTrue( os.path.isfile(tocube) )
        os.remove( tocube )

#@unittest.skip('Takes a while to run hi2isis.')
class Test_getkey(unittest.TestCase):
    def setUp(self):
        self.cub = 'test_getkey.cub'
        isis.hi2isis( img, self.cub )

    def tearDown(self):
        os.remove( self.cub )
        os.remove( 'print.prt' )

    def test_getkey(self):
        truth = 'HIRISE'
        key = isis.getkey( self.cub, 'Instrument', 'InstrumentId' )
        self.assertEqual( truth, key )

    def test_getkey_fail(self):
        # Pixels doesn't have InstrumentId, should fail
        self.assertRaises( subprocess.CalledProcessError, isis.getkey, self.cub, 'Pixels', 'InstrumentId' )

#@unittest.skip('Takes a while to run hi2isis.')
class Test_histat(unittest.TestCase):
    def setUp(self):
        self.cub = 'test_histat.cub'
        isis.hi2isis( img, self.cub )

    def tearDown(self):
        os.remove( self.cub )
        os.remove( 'print.prt' )

    def test_histat_with_to(self):
        tofile = self.cub+'.histat'
        isis.histat( self.cub, to=tofile )
        self.assertTrue( os.path.isfile(tofile) )
        os.remove( tofile )

    def test_histat_without_to(self):
        s = isis.histat( self.cub ).stdout
        self.assertTrue( s.startswith('Group = IMAGE_POSTRAMP') )
