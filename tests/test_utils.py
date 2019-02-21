#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `utils` module."""

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

from pathlib import Path
import unittest
from .utils import resource_check as rc


class TestResources(unittest.TestCase):

    def setUp(self):
        t = Path('tests')
        self.exists1 = t / 'test_kalasiris.py'
        self.exists2 = t / 'test_utils.py'
        self.not1 = t / 'notexists' / 'foo'
        self.not2 = t / 'notexists' / 'foo2'

    def test_have(self):
        (truth, test) = rc(self.exists1, self.exists2)
        self.assertEqual(truth, test)

    def test_have_none(self):
        (truth, test) = rc(self.not1, self.not2)
        self.assertNotEqual(truth, test)

    def test_have_some(self):
        (truth, test) = rc(self.exists1, self.not1)
        self.assertNotEqual(truth, test)
