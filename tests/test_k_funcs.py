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

import kalasiris as isis
from .utils import resource_check as rc


# Hardcoding these, but I sure would like a better solution.
# IsisPreferences = os.path.join('test-resources', 'IsisPreferences')
HiRISE_img = Path('test-resources') / 'PSP_010502_2090_RED5_0.img'


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        (truth, test) = rc(HiRISE_img)
        self.assertEqual(truth, test)


class Test_getkey_k(unittest.TestCase):

    def setUp(self):
        self.cub = Path('test_getkey_k.cub')
        isis.hi2isis(HiRISE_img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

    def test_getkey_k(self):
        truth = 'HIRISE'
        key = isis.getkey_k(self.cub, 'Instrument', 'InstrumentId')
        self.assertEqual(truth, key)


class Test_hi2isis_k(unittest.TestCase):

    def setUp(self):
        self.img = HiRISE_img

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

    def test_with_to(self):
        tocube = Path('test_hi2isis_k.cub')
        isis.hi2isis_k(self.img, to=tocube)
        self.assertTrue(tocube.is_file())
        tocube.unlink()

    def test_without_to(self):
        tocube = Path(self.img).with_suffix('.cub')
        isis.hi2isis_k(self.img)
        self.assertTrue(tocube.is_file())
        tocube.unlink()


class Test_hist_k(unittest.TestCase):

    def setUp(self):
        self.cube = Path('test_hist.cub')
        isis.hi2isis(HiRISE_img, to=self.cube)

    def tearDown(self):
        self.cube.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

    def test_run(self):
        hist_as_string = isis.hist_k(self.cube)
        self.assertTrue(hist_as_string.startswith('Cube'))

    def test_run_with_to(self):
        text_file = Path('test_hist.hist')
        hist_as_string = isis.hist_k(self.cube, to=text_file)
        self.assertTrue(text_file.is_file())
        self.assertTrue(hist_as_string.startswith('Cube'))
        text_file.unlink()

    def test_fail(self):
        # ISIS hist_k needs at least a FROM=, giving it nothing:
        self.assertRaises(subprocess.CalledProcessError, isis.hist_k)
