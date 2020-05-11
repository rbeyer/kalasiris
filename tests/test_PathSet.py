#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `PathSet` class."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib
import unittest
from pathlib import Path

import kalasiris as isis


run_real_files = True
run_real_files_reason = "Tests on real files."


class TestPathSet(unittest.TestCase):
    def setUp(self):
        self.paths = (
            Path("test_PathSet_1.cub"),
            Path("test_PathSet_2.txt"),
            Path("test_PathSet_3.foo"),
        )

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
        self.assertRaises(TypeError, isis.PathSet, "a string")

    def test_add(self):
        ps = isis.PathSet()
        path1 = self.paths[0]
        added_path = ps.add(path1)
        self.assertEqual(path1, added_path)

    def test_add_Error(self):
        ps = isis.PathSet()
        p0 = self.paths[0]
        ps.add(p0)
        self.assertRaises(TypeError, ps.add, "not a Path")
        self.assertRaises(ValueError, ps.add, p0)

    @unittest.skipUnless(run_real_files, run_real_files_reason)
    def test_unlink(self):
        ps = isis.PathSet(self.paths)
        for p in ps:
            p.touch()
        ps.unlink()
        for p in ps:
            self.assertFalse(p.exists())
