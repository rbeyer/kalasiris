#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kalasiris` package."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import kalasiris.kalasiris as isis
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


class TestParams(unittest.TestCase):
    def test_format(self):
        t = ("isisprogram", "from=foo.cub")
        p = {"to": "to.cub", "check": False, "value": 3.0}
        cmd = list(t)
        truth = list(t)
        truth.extend(["to=to.cub", "check=False", "value=3.0"])

        cmd.extend(map(isis.param_fmt, p.keys(), p.values()))
        self.assertEqual(truth, cmd)

    @unittest.skip("Fires up the gui, not sure how to test properly.")
    def test_no_args(self):
        print("\n  about to getkey()")
        isis.getkey()
        # isis.getkey('gui__') does the same thing.
        print("  just got back from getkey()")

    @unittest.skip("Fires up the gui, not sure how to test properly.")
    def test_passthrough(self):
        to_cube = Path("test_passthrough.cub")
        isis.hi2isis(HiRISE_img, to=to_cube)
        print("\n  about to call qview()")
        isis.qview(to_cube)
        print("  just got back from qview()")
        to_cube.unlink()

    def test_reserved_param(self):
        t = "isisprogram"
        p = {"help__": "parameter"}
        cmd = [t]
        truth = [t, "-help=parameter"]

        cmd.extend(map(isis.param_fmt, p.keys(), p.values()))
        self.assertEqual(truth, cmd)

    def test_reserved_nokey(self):
        cp = isis.getkey("help__").stdout.split()

        self.assertEqual("FROM", cp[0])


class Test_Mocks(unittest.TestCase):
    def setUp(self) -> None:
        self.subp_defs = dict(
            check=True,
            env=isis.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

    @patch("kalasiris.kalasiris.subprocess.run")
    def test_subprocess_change_default(self, subp):
        isis.spiceinit("foo.cub", _check=False)
        self.subp_defs["check"] = False
        subp.assert_called_once_with(
            ["spiceinit", "from=foo.cub"], **self.subp_defs
        )

    @patch("kalasiris.kalasiris.subprocess.run")
    def test_subprocess_add(self, subp):
        isis.cam2map("from.cub", to="to.cub", _cwd="foo")
        self.subp_defs.update({"cwd": "foo"})
        subp.assert_called_once_with(
            ["cam2map", "from=from.cub", "to=to.cub"], **self.subp_defs
        )


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_hi2isis(unittest.TestCase):
    def setUp(self):
        self.img = img

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_hi2isis(self):
        tocube = Path("test_hi2isis.cub")
        isis.hi2isis(self.img, to=tocube)
        self.assertTrue(tocube.is_file())
        tocube.unlink()


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_getkey(unittest.TestCase):
    def setUp(self):
        self.cub = Path("test_getkey.cub")
        isis.hi2isis(img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_getkey(self):
        truth = "HIRISE"
        key = isis.getkey(
            self.cub, grpname="Instrument", keyword="InstrumentId"
        ).stdout.strip()
        self.assertEqual(truth, key)

    def test_getkey_fail(self):
        # Pixels doesn't have InstrumentId, should fail
        self.assertRaises(
            subprocess.CalledProcessError,
            isis.getkey,
            self.cub,
            grpname="Pixels",
            keyword="InstrumentId",
        )

    def test_getkey_k_fail(self):
        # Calling getkey with getkey_k syntax will fail
        self.assertRaises(
            IndexError, isis.getkey, self.cub, "Instrument", "InstrumentId"
        )


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_histat(unittest.TestCase):
    def setUp(self):
        self.cub = Path("test_histat.cub")
        isis.hi2isis(img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_histat_with_to(self):
        tofile = self.cub.with_suffix(".histat")
        isis.histat(self.cub, to=tofile)
        self.assertTrue(tofile.is_file())
        tofile.unlink()

    def test_histat_without_to(self):
        s = isis.histat(self.cub).stdout
        self.assertTrue(s.startswith("Group = IMAGE_POSTRAMP"))
