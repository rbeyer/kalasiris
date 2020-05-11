#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions for the test suite."""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import collections
from pathlib import Path


def resource_check(*args):
    """Checks to see if the files exist. And returns a tuple.

       Using the first element as the truth value and the second
       as the test value in a ``self.assertEqual(truth, test)``
       provides a much more useful failure message than a bunch
       of ``self.assertTrue(os.path.isfile(filename))``
    """
    CheckReturn = collections.namedtuple("CheckReturn", ["truth", "test"])

    truth = "Missing Resources:"
    test = truth

    the_missing = []
    for path in map(Path, args):
        if not path.is_file():
            the_missing.append(path)
    if len(the_missing) > 0:
        test = "\n".join(map(lambda x: "    " + str(x), the_missing))
        test += "\n probably just need to 'make test-resources'"

    return CheckReturn(truth, test)
