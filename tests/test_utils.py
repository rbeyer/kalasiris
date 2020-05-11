#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `utils` module."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

from pathlib import Path
import unittest
from .utils import resource_check as rc


class TestResources(unittest.TestCase):
    def setUp(self):
        t = Path("tests")
        self.exists1 = t / "test_kalasiris.py"
        self.exists2 = t / "test_utils.py"
        self.not1 = t / "notexists" / "foo"
        self.not2 = t / "notexists" / "foo2"

    def test_have(self):
        (truth, test) = rc(self.exists1, self.exists2)
        self.assertEqual(truth, test)

    def test_have_none(self):
        (truth, test) = rc(self.not1, self.not2)
        self.assertNotEqual(truth, test)

    def test_have_some(self):
        (truth, test) = rc(self.exists1, self.not1)
        self.assertNotEqual(truth, test)
