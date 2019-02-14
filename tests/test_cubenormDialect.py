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

import csv
import os
import unittest
import kalasiris as isis

# Hardcoding this, but I sure would like a better solution.
img = os.path.join('test-resources', 'HiRISE_test.img')


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        self.assertTrue(os.path.isfile(img))


class TestCubenormDialect(unittest.TestCase):

    def setUp(self):
        self.cube = 'test_cubenorm.cub'
        self.statsfile = 'test_cubenorm.stats'
        isis.hi2isis(img, to=self.cube)
        isis.cubenorm(self.cube, stats=self.statsfile)

    def tearDown(self):
        os.remove('print.prt')
        os.remove(self.cube)
        os.remove(self.statsfile)

    def test_cubenorm_reader(self):
        with open(self.statsfile) as csvfile:
            reader = csv.reader(csvfile, dialect=isis.cubenormDialect)
            for row in reader:
                self.assertEqual(8, len(row))
                break
