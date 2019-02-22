#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `Histogram` class."""

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
import unittest
from pathlib import Path

import kalasiris as isis
from .utils import resource_check as rc


# Hardcoding this, but I sure would like a better solution.
HiRISE_img = Path('test-resources') / 'PSP_010502_2090_RED5_0.img'
img = HiRISE_img


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class TestHistogram(unittest.TestCase):

    def setUp(self):
        self.cube = Path('test_Histogram.cub')
        self.histfile = Path('test_Histogram.hist')
        isis.hi2isis(img, to=self.cube)
        isis.hist(self.cube, to=self.histfile)

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()
        self.cube.unlink()
        self.histfile.unlink()

    def test_init_histfile(self):
        h = isis.Histogram(self.histfile)
        self.assertIsInstance(h, isis.Histogram)

    def test_init_cube(self):
        h = isis.Histogram(self.cube)
        self.assertIsInstance(h, isis.Histogram)

    def test_init_str(self):
        h = isis.Histogram(isis.hist_k(self.cube))
        self.assertIsInstance(h, isis.Histogram)

    def test_dictlike(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(self.cube.name, h['Cube'])

    def test_listlike(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(5, len(h[0]))

    def test_contains(self):
        h = isis.Histogram(self.histfile)
        self.assertTrue('Std Deviation' in h)

    def test_len(self):
        h = isis.Histogram(self.histfile)
        self.assertEqual(107, len(h))
