#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `cubenormDialect` class."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib
import csv
import io
import unittest
from unittest.mock import call, Mock
from pathlib import Path

import kalasiris as isis
from .utils import resource_check as rc


run_real_files = True
run_real_files_reason = "Tests on real files, and runs ISIS."

# Hardcoding this, but I sure would like a better solution.
img = Path("test-resources") / "PSP_010502_2090_RED5_0.img"


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestResources(unittest.TestCase):
    """Establishes that the test image exists."""

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class TestCubenormFile(unittest.TestCase):
    def setUp(self):
        self.stats = (
            "    Band  RowCol    ValidPoints        Average         "
            "Median         StdDev        Minimum        Maximum\n"
            "       1       1           4000        6532.67           "
            "6526         191.58           5790           7211\n"
            "       1       2           4000        6296.87           "
            "6303        187.865           5501           6980\n"
            "       1       3           4000        6341.42           "
            "6378        188.321           5465           7026\n"
            "       1       4           4000        6381.09           "
            "6415        187.721           5429           6980\n"
            "       1       5           4000        6391.85           "
            "6415        184.816           5537           7026\n"
            "       1       6           4000        6411.03           "
            "6415        184.951           5465           7073\n"
        )

    def test_Dialect(self):
        reader = csv.reader(
            self.stats.splitlines(), dialect=isis.cubenormfile.Dialect
        )
        for row in reader:
            self.assertEqual(8, len(row))
            break

    def test_writer(self):
        columns = list()
        reader = csv.reader(
            self.stats.splitlines(), dialect=isis.cubenormfile.Dialect
        )
        for row in reader:
            columns.append(row)

        csvfile = Mock()
        writer = isis.cubenormfile.writer(csvfile)
        for row in columns:
            writer.writerow(row)

        expected = list()
        for line in self.stats.splitlines(True):
            expected.append(call.write(line))

        self.assertEqual(csvfile.method_calls, expected)

    def test_DictWriter(self):
        columns = list()
        reader = csv.DictReader(
            self.stats.splitlines(), dialect=isis.cubenormfile.Dialect
        )
        for row in reader:
            columns.append(row)

        csvfile = Mock()
        writer = isis.cubenormfile.DictWriter(csvfile)
        writer.writeheader()
        for row in columns:
            writer.writerow(row)

        expected = list()
        for line in self.stats.splitlines(True):
            expected.append(call.write(line))

        self.assertEqual(csvfile.method_calls, expected)


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestCubenormFile_filesystem(unittest.TestCase):
    def setUp(self):
        self.cube = Path("test_cubenormfile.cub")
        self.statsfile = Path("test_cubenormfile.stats")
        isis.hi2isis(img, to=self.cube)
        isis.cubenorm(self.cube, stats=self.statsfile)

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()
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

        outfile = self.statsfile.with_suffix(".writer.stats")
        with open(outfile, "w") as csvfile:
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
