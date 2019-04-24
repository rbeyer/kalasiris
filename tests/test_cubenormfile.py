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

import contextlib
import csv
import io
import unittest
from pathlib import Path

import kalasiris as isis
from .utils import resource_check as rc

# Hardcoding this, but I sure would like a better solution.
img = Path('test-resources') / 'PSP_010502_2090_RED5_0.img'


class TestResources(unittest.TestCase):
    '''Establishes that the test image exists.'''

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class TestCubenormFile(unittest.TestCase):

    def setUp(self):
        self.cube = Path('test_cubenormfile.cub')
        self.statsfile = Path('test_cubenormfile.stats')
        isis.hi2isis(img, to=self.cube)
        isis.cubenorm(self.cube, stats=self.statsfile)

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path('print.prt').unlink()
        self.cube.unlink()
        self.statsfile.unlink()

    def test_Dialect(self):
        with open(self.statsfile) as csvfile:
            reader = csv.reader(csvfile, dialect=isis.cubenormfile.Dialect)
            for row in reader:
                self.assertEqual(8, len(row))
                break

    def test_writer(self):
        columns = list()
        with open(self.statsfile) as csvfile:
            reader = csv.reader(csvfile, dialect=isis.cubenormfile.Dialect)
            for row in reader:
                columns.append(row)

        outfile = self.statsfile.with_suffix('.writer.stats')
        with open(outfile, 'w') as csvfile:
            writer = isis.cubenormfile.writer(csvfile)
            for row in columns:
                writer.writerow(row)

        with open(self.statsfile) as in_file:
            with open(outfile) as out_file:
                for i, o in zip(in_file.readlines(), out_file.readlines()):
                    with self.subTest(inputline=i, outputline=o):
                        self.assertEqual(i, o)
        outfile.unlink()

    def test_DictWriter(self):
        columns = list()
        with open(self.statsfile) as csvfile:
            reader = csv.DictReader(csvfile, dialect=isis.cubenormfile.Dialect)
            for row in reader:
                columns.append(row)

        with io.StringIO() as out_file:
            writer = isis.cubenormfile.DictWriter(out_file)
            writer.writeheader()
            for row in columns:
                writer.writerow(row)

            with open(self.statsfile) as in_file:
                for i, o in zip(in_file.readlines(), out_file.readlines()):
                    with self.subTest(inputline=i, outputline=o):
                        self.assertEqual(i, o)
