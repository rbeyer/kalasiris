#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kalasiris` package."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import importlib
import os
import unittest
import kalasiris.kalasiris


class TestHOME(unittest.TestCase):
    """Not all platforms have a $HOME environment variable."""

    def test_HOME(self):
        if "HOME" in os.environ:
            del os.environ["HOME"]

        self.assertTrue(importlib.reload(kalasiris.kalasiris))
