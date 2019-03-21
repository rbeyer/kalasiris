#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `PathSet` class."""

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


class TestPathSet(unittest.TestCase):

    def setUp(self):
        self.paths = (Path('test_PathSet_1.cub'),
                      Path('test_PathSet_2.txt'),
                      Path('test_PathSet_3.foo'))

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            for p in self.paths:
                p.unlink()

    def test_init(self):
        ps = isis.PathSet()
        self.assertIsInstance(ps, isis.PathSet)

    def test_init_iterable(self):
        ps = isis.PathSet(self.paths)
        self.assertEqual(3, len(ps))

    def test_init_fail(self):
        self.assertRaises(TypeError, isis.PathSet, 'a string')

    def test_add(self):
        ps = isis.PathSet()
        path1 = self.paths[0]
        added_path = ps.add(path1)
        self.assertEqual(path1, added_path)

    def test_unlink(self):
        ps = isis.PathSet(self.paths)
        for p in ps:
            p.touch()
        ps.unlink()
        for p in ps:
            self.assertFalse(p.exists())
