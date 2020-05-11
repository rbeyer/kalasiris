#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `version` module."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import datetime
import unittest

import kalasiris.version as version


class TestVersion(unittest.TestCase):
    def test_get_from_string(self):
        s = [
            (
                """3.7.0        # Public version number
2019-04-30   # Release date
stable       # release stage (alpha, beta, stable)""",
                version.ISISversion(
                    3, 7, 0, "stable", datetime.date(2019, 4, 30)
                ),
            ),
            (
                """3.6.0        # Public version number
10-26-2018   # Release date
stable         # release stage (alpha, beta, stable)""",
                version.ISISversion(
                    3, 6, 0, "stable", datetime.date(2018, 10, 26)
                ),
            ),
            (
                """3.5.2.0
2018-04-06   # Version date
v007         # 3rd party libraries version
stable       # release stage (alpha, beta, stable)""",
                version.ISISversion(
                    3, 5, 2, "stable", datetime.date(2018, 4, 6)
                ),
            ),
        ]

        for v in s:
            with self.subTest(v=v[1]):
                self.assertEqual(v[1], version.get_from_string(v[0]))

    def test_fail_from_string(self):
        s = "No version here."
        self.assertRaises(ValueError, version.get_from_string, s)

    @unittest.skip("Not a robust test, only occaisional.")
    def test_version_info(self):
        # Who knows what version of ISIS will be loaded, this
        # is just for occaisionally testing this functionality.
        print(version.version_info())
