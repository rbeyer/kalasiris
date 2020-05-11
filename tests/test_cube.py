#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `cube` module."""

# Copyright 2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib
import unittest
from pathlib import Path

import kalasiris as isis
from .utils import resource_check as rc

run_real_files = True
run_real_files_reason = "Tests on real files, and runs ISIS."

# Hardcoding this, but I sure would like a better solution.
HiRISE_img = Path("test-resources") / "PSP_010502_2090_RED5_0.img"
img = HiRISE_img


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestResources(unittest.TestCase):
    """Establishes that the test image exists."""

    def test_resources(self):
        (truth, test) = rc(img)
        self.assertEqual(truth, test)


class TestBasic(unittest.TestCase):
    def test_get_start_size(self):
        d = {"StartByte": "10", "Bytes": "20"}
        self.assertEqual((9, 20), isis.cube._get_start_size(d))


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestTable(unittest.TestCase):
    def setUp(self):
        self.cube = Path("test_TableRead.cub")
        isis.hi2isis(img, to=self.cube)

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()
        self.cube.unlink()

    def test_read_table_data(self):
        self.assertRaises(ValueError, isis.cube.read_table_data, self.cube)
        self.assertRaises(
            KeyError,
            isis.cube.read_table_data,
            self.cube,
            table_name="Non-Existant Table Name",
        )

        table_bytes = isis.cube.read_table_data(
            self.cube, table_name="HiRISE Calibration Ancillary"
        )
        self.assertEqual(7440, len(table_bytes))

        label = {"StartByte": "4169490", "Bytes": "126976"}
        table_bytes = isis.cube.read_table_data(self.cube, label=label)
        self.assertEqual(int(label["Bytes"]), len(table_bytes))

    def test_parse_table(self):
        table_bytes = isis.cube.read_table_data(
            self.cube, table_name="HiRISE Calibration Ancillary"
        )

        fields = [
            {"Name": "GapFlag", "Type": "Integer", "Size": "1"},
            {"Name": "LineNumber", "Type": "Integer", "Size": "1"},
            {"Name": "BufferPixels", "Type": "Integer", "Size": "12"},
            {"Name": "DarkPixels", "Type": "Integer", "Size": "16"},
        ]

        table = isis.cube.parse_table(table_bytes, fields)

        self.assertEqual(255, table["GapFlag"][0])
        self.assertEqual(9, table["LineNumber"][9])
        self.assertEqual(1359, table["BufferPixels"][0][0])
        self.assertEqual(1290, table["DarkPixels"][0][9])

    def test_get_table(self):
        try:
            import pvl  # noqa F401

            table = isis.cube.get_table(
                self.cube, "HiRISE Calibration Ancillary"
            )
            self.assertEqual(255, table["GapFlag"][0])
            self.assertEqual(9, table["LineNumber"][9])
            self.assertEqual(1359, table["BufferPixels"][0][0])
            self.assertEqual(1290, table["DarkPixels"][0][9])

        except ImportError:
            self.assertRaises(
                ImportError,
                isis.cube.get_table,
                self.cube,
                "HiRISE Calibration Ancillary",
            )

    def test_overwrite_table_data(self):
        data = bytes(10)
        self.assertRaises(
            ValueError, isis.cube.overwrite_table_data, self.cube, data
        )
        self.assertRaises(
            KeyError,
            isis.cube.overwrite_table_data,
            self.cube,
            data,
            table_name="Non-Existant Table Name",
        )
        self.assertRaises(
            ValueError,
            isis.cube.overwrite_table_data,
            self.cube,
            data,
            table_name="HiRISE Calibration Ancillary",
        )

        # Write zeros into the table:
        table_data = bytes(7440)
        isis.cube.overwrite_table_data(
            self.cube, table_data, table_name="HiRISE Calibration Ancillary"
        )

        # Read the table back, verify a zero:
        table_bytes = isis.cube.read_table_data(
            self.cube, table_name="HiRISE Calibration Ancillary"
        )
        fields = [
            {"Name": "A", "Type": "Integer", "Size": "1"},
            {"Name": "B", "Type": "Integer", "Size": "1"},
            {"Name": "C", "Type": "Integer", "Size": "12"},
            {"Name": "D", "Type": "Integer", "Size": "16"},
        ]
        table = isis.cube.parse_table(table_bytes, fields)
        self.assertEqual(0, table["C"][0][0])

    def test_encode_table(self):
        table = {
            "Foo": [1, 2, 3, 4],
            "Bar": [1.1, 2.2, 3.3, 4.4],
            "Boo": ["a", "b", "c", "d"],
        }
        fields = [
            {"Name": "Foo", "Type": "Integer", "Size": "1"},
            {"Name": "Bar", "Type": "Real", "Size": "1"},
            {"Name": "Boo", "Type": "Text", "Size": "1"},
        ]

        bad_table = dict(table)
        bad_table["TooLong"] = ["a", "b", "c", "d", "e"]
        self.assertRaises(
            IndexError, isis.cube.encode_table, bad_table, fields
        )

        bad_fields = list(fields)
        bad_fields.append({"Name": "TooLong", "Type": "Text", "Size": "1"})
        self.assertRaises(KeyError, isis.cube.encode_table, table, bad_fields)

        data = isis.cube.encode_table(table, fields)
        # print(len(data))
        # print(data)

        parsed_tab = isis.cube.parse_table(data, fields)
        # print(tab)
        self.assertEqual(table["Foo"], parsed_tab["Foo"])

    def test_overwrite_table(self):
        table_bytes = isis.cube.read_table_data(
            self.cube, table_name="HiRISE Calibration Ancillary"
        )

        fields = [
            {"Name": "GapFlag", "Type": "Integer", "Size": "1"},
            {"Name": "LineNumber", "Type": "Integer", "Size": "1"},
            {"Name": "BufferPixels", "Type": "Integer", "Size": "12"},
            {"Name": "DarkPixels", "Type": "Integer", "Size": "16"},
        ]

        table = isis.cube.parse_table(table_bytes, fields)

        for i, ln in enumerate(table["LineNumber"]):
            table["LineNumber"][i] = 27

        try:
            import pvl  # noqa F401

            isis.cube.overwrite_table(
                self.cube, "HiRISE Calibration Ancillary", table
            )

            p_tab = isis.cube.get_table(
                self.cube, "HiRISE Calibration Ancillary"
            )

            self.assertEqual(255, p_tab["GapFlag"][0])
            self.assertEqual(27, p_tab["LineNumber"][9])
            self.assertEqual(1359, p_tab["BufferPixels"][0][0])
            self.assertEqual(1290, p_tab["DarkPixels"][0][9])

        except ImportError:
            self.assertRaises(
                ImportError,
                isis.cube.overwrite_table,
                self.cube,
                "HiRISE Calibration Ancillary",
                table,
            )
