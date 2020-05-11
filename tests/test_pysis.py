#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the pysis emulation module."""

# Copyright 2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib

# import subprocess
import unittest
from pathlib import Path

import kalasiris.pysis as pysis
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


class Test_get_isis_program_names(unittest.TestCase):
    @unittest.skipUnless(run_real_files, run_real_files_reason)
    def test_get_names(self):
        self.assertIn("cam2map", dir(pysis))


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_hi2isis(unittest.TestCase):
    def setUp(self):
        self.img = img

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_hi2isis(self):
        tocube = Path("test_hi2isis.cub")
        pysis.hi2isis(self.img, to=tocube)
        self.assertTrue(tocube.is_file())
        tocube.unlink()


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_getkey(unittest.TestCase):
    def setUp(self):
        self.cub = Path("test_getkey.cub")
        pysis.hi2isis(img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_getkey(self):
        truth = b"HIRISE\n"
        key = pysis.getkey(
            self.cub, grpname="Instrument", keyword="InstrumentId"
        )
        self.assertEqual(truth, key)

    def test_getkey_fail(self):
        # Pixels doesn't have InstrumentId, should fail
        self.assertRaises(
            pysis.ProcessError,
            pysis.getkey,
            self.cub,
            grpname="Pixels",
            keyword="InstrumentId",
        )

    def test_getkey_k_fail(self):
        # Calling getkey with getkey_k syntax will fail
        self.assertRaises(
            IndexError, pysis.getkey, self.cub, "Instrument", "InstrumentId"
        )
