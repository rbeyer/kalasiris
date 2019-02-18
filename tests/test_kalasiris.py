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

import os
import subprocess
import unittest
import kalasiris.kalasiris as isis


# Hardcoding this, but I sure would like a better solution.
img = os.path.join('test-resources', 'PSP_010502_2090_RED5_0.img')


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        self.assertTrue(os.path.isfile(img))


class TestParams(unittest.TestCase):

    def test_param_fmt(self):
        t = ('isisprogram', 'from=foo.cub')
        p = {'to': 'to.cub', 'check': False, 'value': 3.0}
        cmd = list(t)
        truth = list(t)
        truth.extend(['to=to.cub', 'check=False', 'value=3.0'])

        cmd.extend(map(isis.param_fmt, p.keys(), p.values()))
        self.assertEqual(truth, cmd)

    @unittest.skip('Will fire up the gui, not sure how to test properly.')
    def test_no_args(self):
        print('about to getkey()')
        isis.getkey()
        # isis.getkey('gui__') does the same thing.
        print('just got back from getkey()')

    def test_reserved_param(self):
        t = 'isisprogram'
        p = {'help__': 'parameter'}
        cmd = [t]
        truth = [t]
        truth.append('-help=parameter')

        cmd.extend(map(isis.param_fmt, p.keys(), p.values()))
        self.assertEqual(truth, cmd)

    def test_reserved_nokey(self):
        cp = isis.getkey('help__').stdout.split()

        self.assertEqual('FROM', cp[0])


class Test_get_isis_program_names(unittest.TestCase):

    def test_get_names(self):
        # for n in isis._get_isis_program_names():
        #     print(n)
        # s = sum(1 for _ in isis._get_isis_program_names())
        # print(f'How many programs: {s}')
        self.assertIn('cam2map', isis._get_isis_program_names())


# @unittest.skip('Can take a while to run hi2isis.')
class Test_hi2isis(unittest.TestCase):

    def setUp(self):
        self.img = img

    def tearDown(self):
        os.remove('print.prt')

    def test_hi2isis(self):
        tocube = 'test_hi2isis.cub'
        isis.hi2isis(self.img, to=tocube)
        self.assertTrue(os.path.isfile(tocube))
        os.remove(tocube)


class Test_getkey(unittest.TestCase):

    def setUp(self):
        self.cub = 'test_getkey.cub'
        isis.hi2isis(img, to=self.cub)

    def tearDown(self):
        os.remove(self.cub)
        os.remove('print.prt')

    def test_getkey(self):
        truth = 'HIRISE'
        key = isis.getkey(self.cub, grpname='Instrument',
                          keyword='InstrumentId').stdout.strip()
        self.assertEqual(truth, key)

    def test_getkey_fail(self):
        # Pixels doesn't have InstrumentId, should fail
        self.assertRaises(subprocess.CalledProcessError,
                          isis.getkey, self.cub,
                          grpname='Pixels', keyword='InstrumentId')

    def test_getkey_k_fail(self):
        # Calling getkey with getkey_k syntax will fail
        self.assertRaises(IndexError,
                          isis.getkey, self.cub,
                          'Instrument', 'InstrumentId')


class Test_histat(unittest.TestCase):

    def setUp(self):
        self.cub = 'test_histat.cub'
        isis.hi2isis(img, to=self.cub)

    def tearDown(self):
        os.remove(self.cub)
        os.remove('print.prt')

    def test_histat_with_to(self):
        tofile = self.cub + '.histat'
        isis.histat(self.cub, to=tofile)
        self.assertTrue(os.path.isfile(tofile))
        os.remove(tofile)

    def test_histat_without_to(self):
        s = isis.histat(self.cub).stdout
        self.assertTrue(s.startswith('Group = IMAGE_POSTRAMP'))
