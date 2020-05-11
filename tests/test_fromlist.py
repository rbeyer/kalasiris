#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `fromlist` class."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib
import os
import unittest
from unittest.mock import Mock, patch
from pathlib import Path

import kalasiris as isis


run_real_files = True
run_real_files_reason = "Tests on real files."


class TestFromList(unittest.TestCase):
    def setUp(self):
        self.list = ["a.cub", "b.cub", "c.cub"]

    @patch("kalasiris.fromlist.builtins.print")
    def test_print(self, m_print):
        isis.fromlist.print(self.list)
        self.assertEqual(m_print.call_args_list[0][0][0], self.list[0])
        self.assertEqual(m_print.call_args_list[1][0][0], self.list[1])
        self.assertEqual(m_print.call_args_list[2][0][0], self.list[2])

    @patch("kalasiris.fromlist.builtins.print")
    def test_print_fl(self, m_print):
        isis.fromlist.print_fl(self.list)
        self.assertEqual(m_print.call_args_list[0][0][0], self.list[0])
        self.assertEqual(m_print.call_args_list[1][0][0], self.list[1])
        self.assertEqual(m_print.call_args_list[2][0][0], self.list[2])

    @patch("kalasiris.fromlist.print_fl")
    def test_make(self, m_print_fl):
        m_filelike = Mock()
        m_filelike.name = "dummy.txt"
        with patch(
            "kalasiris.fromlist.tempfile.NamedTemporaryFile",
            return_value=m_filelike,
        ):
            temp_file = isis.fromlist.make(self.list)
            self.assertEqual(temp_file, Path(m_filelike.name))
            m_print_fl.called_once_with(self.list, file=m_filelike)

    @patch("kalasiris.fromlist.print_fl")
    def test_make_wfile(self, m_print_fl):
        m_filelike = Mock()
        m_filelike.name = "dummy.txt"
        with patch("kalasiris.fromlist.open", return_value=m_filelike):
            temp_file = isis.fromlist.make(self.list, m_filelike.name)
            self.assertEqual(temp_file, Path(m_filelike.name))
            m_print_fl.called_once_with(self.list, file=m_filelike)


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestFromList_filesystem(unittest.TestCase):
    def setUp(self):
        self.list = ["a.cub", "b.cub", "c.cub"]
        self.text = "a.cub\nb.cub\nc.cub\n"
        self.path = Path("test_fromlist.txt")

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            self.path.unlink()

    def test_print(self):
        with open(self.path, "w") as f:
            isis.fromlist.print(self.list, f)
        self.assertTrue(self.path.exists())
        self.assertEqual(self.path.read_text(), self.text)

    def test_print_fl(self):
        with open(self.path, "w") as f:
            isis.fromlist.print_fl(self.list, f)
        self.assertTrue(self.path.exists())
        self.assertEqual(self.path.read_text(), self.text)

    def test_make(self):
        temp_file = isis.fromlist.make(self.list)
        self.assertTrue(temp_file.exists())
        self.assertEqual(temp_file.read_text(), self.text)
        temp_file.unlink()

    def test_make_wfile(self):
        isis.fromlist.make(self.list, self.path)
        self.assertTrue(self.path.exists())
        self.assertEqual(self.path.read_text(), self.text)

    def test_open_fl(self):
        with isis.fromlist.open_fl(self.list) as f:
            self.assertEqual(f.read(), self.text)
            filename = f.name
        self.assertFalse(os.path.exists(filename))

    def test_open_fl_wfile(self):
        with isis.fromlist.open_fl(self.list, self.path) as f:
            self.assertEqual(f.read(), self.text)
        self.assertTrue(self.path.exists())

    def test_temp(self):
        with isis.fromlist.temp(self.list) as f:
            self.assertEqual(f.read_text(), self.text)
            filename = f
            self.assertTrue(filename.exists())
        self.assertFalse(filename.exists())
