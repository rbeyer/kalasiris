#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sweetened` module."""

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
import shutil
import unittest
from pathlib import Path

import kalasiris.sweetened as isis
from .utils import resource_check as rc


# Hardcoding this, but I sure would like a better solution.
HiRISE_img = Path('test-resources') / 'PSP_010502_2090_RED5_0.img'
img = HiRISE_img


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class Test_hi2isis(unittest.TestCase):

    def setUp(self):
        self.img = img

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

    def test_hi2isis_with_to(self):
        tocube = Path('test_sweetened_hi2isis.cub')
        isis.hi2isis(self.img, to=tocube)
        self.assertTrue(tocube.is_file())
        tocube.unlink()

    def test_hi2isis_without_to(self):
        sweet_img = self.img.with_name('sweet.img')
        shutil.copy(self.img, sweet_img)
        tocube = sweet_img.with_suffix('.cub')
        isis.hi2isis(sweet_img)
        self.assertTrue(tocube.is_file())
        tocube.unlink()
        sweet_img.unlink()


class Test_getkey(unittest.TestCase):

    def setUp(self):
        self.cub = Path('test_sweetened_getkey.cub')
        isis.hi2isis(HiRISE_img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()

    def test_getkey_k(self):
        truth = 'HIRISE'
        key = isis.getkey(self.cub, 'Instrument', 'InstrumentId')
        self.assertEqual(truth, key)
