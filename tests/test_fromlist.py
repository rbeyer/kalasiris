#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `fromlist` class."""

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
import os
import unittest
from unittest.mock import Mock, patch
from pathlib import Path

import kalasiris as isis


run_real_files = True
run_real_files_reason = 'Tests on real files.'


class TestFromList(unittest.TestCase):

    def setUp(self):
        self.list = ['a.cub', 'b.cub', 'c.cub']

    @patch('kalasiris.fromlist.builtins.print')
    def test_print(self, m_print):
        isis.fromlist.print(self.list)
        self.assertEqual(m_print.call_args_list[0][0][0], self.list[0])
        self.assertEqual(m_print.call_args_list[1][0][0], self.list[1])
        self.assertEqual(m_print.call_args_list[2][0][0], self.list[2])
        self.assertEqual(m_print.call_args_list[3][0][0], '')

    @patch('kalasiris.fromlist.builtins.print')
    def test_print_fl(self, m_print):
        isis.fromlist.print_fl(self.list)
        self.assertEqual(m_print.call_args_list[0][0][0], self.list[0])
        self.assertEqual(m_print.call_args_list[1][0][0], self.list[1])
        self.assertEqual(m_print.call_args_list[2][0][0], self.list[2])
        self.assertEqual(m_print.call_args_list[3][0][0], '')

    @patch('kalasiris.fromlist.print_fl')
    def test_make(self, m_print_fl):
        m_filelike = Mock()
        m_filelike.name = 'dummy.txt'
        with patch('kalasiris.fromlist.tempfile.NamedTemporaryFile',
                   return_value=m_filelike):
            temp_file = isis.fromlist.make(self.list)
            self.assertEqual(temp_file, Path(m_filelike.name))
            m_print_fl.called_once_with(self.list, file=m_filelike)

    @patch('kalasiris.fromlist.print_fl')
    def test_make_wfile(self, m_print_fl):
        m_filelike = Mock()
        m_filelike.name = 'dummy.txt'
        with patch('kalasiris.fromlist.open', return_value=m_filelike):
            temp_file = isis.fromlist.make(self.list, m_filelike.name)
            self.assertEqual(temp_file, Path(m_filelike.name))
            m_print_fl.called_once_with(self.list, file=m_filelike)


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestFromList_filesystem(unittest.TestCase):

    def setUp(self):
        self.list = ['a.cub', 'b.cub', 'c.cub']
        self.text = 'a.cub\nb.cub\nc.cub\n\n'
        self.path = Path('test_fromlist.txt')

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            self.path.unlink()

    def test_print(self):
        with open(self.path, 'w') as f:
            isis.fromlist.print(self.list, f)
        self.assertTrue(self.path.exists())
        self.assertEqual(self.path.read_text(), self.text)

    def test_print_fl(self):
        with open(self.path, 'w') as f:
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
