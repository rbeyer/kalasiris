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

import contextlib
import subprocess
import unittest
from pathlib import Path

from kalasiris.kalasiris import _get_isis_program_names as gipn
import kalasiris.kalasiris as isis
from .utils import resource_check as rc


# Hardcoding this, but I sure would like a better solution.
HiRISE_img = Path('test-resources') / 'PSP_010502_2090_RED5_0.img'
img = HiRISE_img


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class TestParams(unittest.TestCase):

    def test_format(self):
        t = ('isisprogram', 'from=foo.cub')
        p = {'to': 'to.cub', 'check': False, 'value': 3.0}
        cmd = list(t)
        truth = list(t)
        truth.extend(['to=to.cub', 'check=False', 'value=3.0'])

        cmd.extend(map(isis.param_fmt, p.keys(), p.values()))
        self.assertEqual(truth, cmd)

    @unittest.skip('Fires up the gui, not sure how to test properly.')
    def test_no_args(self):
        print('\n  about to getkey()')
        isis.getkey()
        # isis.getkey('gui__') does the same thing.
        print('  just got back from getkey()')

    @unittest.skip('Fires up the gui, not sure how to test properly.')
    def test_passthrough(self):
        to_cube = Path('test_passthrough.cub')
        isis.hi2isis(HiRISE_img, to=to_cube)
        print('\n  about to call qview()')
        isis.qview(to_cube)
        print('  just got back from qview()')
        to_cube.unlink()

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
        # for n in gipn():
        #     print(n)
        # s = sum(1 for _ in gipn())
        # print(f'How many programs: {s}')
        self.assertIn('cam2map', gipn())


# @unittest.skip('Can take a while to run hi2isis.')
class Test_hi2isis(unittest.TestCase):

    def setUp(self):
        self.img = img

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

    def test_hi2isis(self):
        tocube = Path('test_hi2isis.cub')
        isis.hi2isis(self.img, to=tocube)
        self.assertTrue(tocube.is_file())
        tocube.unlink()


class Test_getkey(unittest.TestCase):

    def setUp(self):
        self.cub = Path('test_getkey.cub')
        isis.hi2isis(img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

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
        self.cub = Path('test_histat.cub')
        isis.hi2isis(img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

    def test_histat_with_to(self):
        tofile = self.cub.with_suffix('.histat')
        isis.histat(self.cub, to=tofile)
        self.assertTrue(tofile.is_file())
        tofile.unlink()

    def test_histat_without_to(self):
        s = isis.histat(self.cub).stdout
        self.assertTrue(s.startswith('Group = IMAGE_POSTRAMP'))
