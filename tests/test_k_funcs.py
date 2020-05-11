#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kalasiris` package."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import contextlib
import os
import subprocess
import unittest
from unittest.mock import call, patch, MagicMock, Mock
from pathlib import Path

import kalasiris as isis
from .utils import resource_check as rc


# Hardcoding these, but I sure would like a better solution.
# IsisPreferences = os.path.join('test-resources', 'IsisPreferences')
HiRISE_img = Path("test-resources") / "PSP_010502_2090_RED5_0.img"
run_real_files = True
run_real_files_reason = "Tests on real files, and runs ISIS."


@unittest.skipUnless(run_real_files, run_real_files_reason)
class TestResources(unittest.TestCase):
    """Establishes that the test image exists."""

    def test_resources(self):
        (truth, test) = rc(HiRISE_img)
        self.assertEqual(truth, test)


class Test_getkey_k(unittest.TestCase):
    def test_getkey_k(self):
        truth = "HIRISE"
        gk = Mock(stdout=f"{truth}\n")
        with patch("kalasiris.k_funcs.isis.getkey", return_value=gk):
            key = isis.getkey_k("dummy.cub", "Instrument", "InstrumentId")
            self.assertEqual(truth, key)


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_getkey_k_filesystem(unittest.TestCase):
    def setUp(self):
        self.cub = Path("test_getkey_k.cub")
        isis.hi2isis(HiRISE_img, to=self.cub)

    def tearDown(self):
        self.cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_getkey_k(self):
        truth = "HIRISE"
        key = isis.getkey_k(self.cub, "Instrument", "InstrumentId")
        self.assertEqual(truth, key)


class Test_hi2isis_k(unittest.TestCase):
    @patch("kalasiris.k_funcs.isis.hi2isis")
    def test_with_to(self, m_hi2i):
        isis.hi2isis_k("dummy.img", to="dummy.cub")
        self.assertEqual(
            m_hi2i.call_args_list, [call("dummy.img", to="dummy.cub")]
        )

    @patch("kalasiris.k_funcs.isis.hi2isis")
    def test_without_to(self, m_hi2i):
        isis.hi2isis_k("dummy.img")
        self.assertEqual(
            m_hi2i.call_args_list, [call("dummy.img", to=Path("dummy.cub"))]
        )


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_hi2isis_k_filesystem(unittest.TestCase):
    def setUp(self):
        self.img = HiRISE_img

    def tearDown(self):
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_with_to(self):
        tocube = Path("test_hi2isis_k.cub")
        isis.hi2isis_k(self.img, to=tocube)
        self.assertTrue(tocube.is_file())
        tocube.unlink()

    def test_without_to(self):
        tocube = Path(self.img).with_suffix(".cub")
        isis.hi2isis_k(self.img)
        self.assertTrue(tocube.is_file())
        tocube.unlink()


class Test_hist_k(unittest.TestCase):
    @patch("kalasiris.k_funcs.isis.hist")
    def test_run(self, m_hist):
        hist_txt = "This is hist output."
        filelike = Mock()
        filelike.read = Mock(return_value=hist_txt)
        with patch(
            "kalasiris.k_funcs.isis.tempfile.NamedTemporaryFile",
            return_value=filelike,
        ):
            hist_as_string = isis.hist_k("dummy.cub")
            self.assertEqual(hist_as_string, hist_txt)

    def test_fail(self):
        # ISIS hist_k needs at least a FROM=, giving it nothing:
        self.assertRaises(subprocess.CalledProcessError, isis.hist_k)


@unittest.skipUnless(run_real_files, run_real_files_reason)
class Test_hist_k_filesystem(unittest.TestCase):
    def setUp(self):
        self.cube = Path("test_hist.cub")
        isis.hi2isis(HiRISE_img, to=self.cube)

    def tearDown(self):
        self.cube.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()

    def test_run(self):
        hist_as_string = isis.hist_k(self.cube)
        self.assertTrue(hist_as_string.startswith("Cube"))

    def test_run_with_to(self):
        text_file = Path("test_hist.hist")
        hist_as_string = isis.hist_k(self.cube, to=text_file)
        self.assertTrue(text_file.is_file())
        self.assertTrue(hist_as_string.startswith("Cube"))
        text_file.unlink()


class Test_stats_k(unittest.TestCase):
    def test_stats_k(self):
        stats_text = """Group = Results
  From                    = PSP_010502_2090_RED4_1.cub
  Band                    = 1
  Average                 = 6498.477293457
  StandardDeviation       = 181.94624138776
  Variance                = 33104.434755134
  Median                  = 6497.0
  Mode                    = 6534.0
  Skew                    = 0.024358185897602
  Minimum                 = 4117.0
  Maximum                 = 8207.0
  Sum                     = 13308881497.0
  TotalPixels             = 2048000
  ValidPixels             = 2048000
  OverValidMaximumPixels  = 0
  UnderValidMinimumPixels = 0
  NullPixels              = 0
  LisPixels               = 0
  LrsPixels               = 0
  HisPixels               = 0
  HrsPixels               = 0
End_Group
"""
        cp = Mock(stdout=stats_text)
        with patch("kalasiris.k_funcs.isis.stats", return_value=cp):
            d = isis.stats_k("foo")
            self.assertEqual(20, len(d))
            self.assertEqual(d["Average"], "6498.477293457")

    @unittest.skipUnless(run_real_files, run_real_files_reason)
    def test_stats_k_file(self):
        cub = Path("test_stats_k.cub")
        isis.hi2isis(HiRISE_img, to=cub)

        d = isis.stats_k(cub)
        self.assertEqual(d["TotalPixels"], "2048000")

        cub.unlink()
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()


class Test_cubeit_k(unittest.TestCase):
    @patch("kalasiris.k_funcs.isis.cubeit")
    def test_cubeit_k(self, m_cubeit):
        from_name = "temp_fromlist.txt"
        m_context = Mock(
            __enter__=Mock(return_value=from_name), __exit__=Mock()
        )
        m_temp = MagicMock(return_value=m_context)
        with patch("kalasiris.k_funcs.isis.fromlist.temp", m_temp):
            isis.cubeit_k(["a.cub", "b.cub", "c.cub"], to="stacked.cub")
            m_temp.assert_called_with(["a.cub", "b.cub", "c.cub"])
            self.assertEqual(
                m_cubeit.call_args_list,
                [call(fromlist=from_name, to="stacked.cub")],
            )

    @unittest.skipUnless(run_real_files, run_real_files_reason)
    def test_cubeit_k_files(self):
        a_cube = "test_cubeit_a.cub"
        isis.makecube(to=a_cube, value=1, samples=2, lines=2, bands=1)
        b_cube = "test_cubeit_b.cub"
        isis.makecube(to=b_cube, value=1, samples=2, lines=2, bands=1)
        c_cube = "test_cubeit_c.cub"
        isis.makecube(to=c_cube, value=1, samples=2, lines=2, bands=1)
        s_cube = "test_cubeit_stacked.cub"
        isis.cubeit_k([a_cube, b_cube, c_cube], to=s_cube)
        for f in (a_cube, b_cube, c_cube, s_cube):
            os.unlink(f)
        with contextlib.suppress(FileNotFoundError):
            Path("print.prt").unlink()
