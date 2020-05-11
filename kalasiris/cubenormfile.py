#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The ISIS ``cubenorm`` program outputs plain text table information and
also reads it in, but the format is a very specific fixed-width
table format.  A plain :func:`csv.reader` or :func:`csv.DictReader` using
the :class:`.cubenormfile.Dialect` object will be able to read the text
output of ``cubenorm``, but to write out a file that ``cubenorm`` will
read in, you will need to use the :class:`.cubenormfile.writer` or
:class:`.cubenormfile.DictWriter` classes.
"""

# Copyright 2019-2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import csv

# Establish the allowable cubenorm fieldnames and their character widths.
fieldnames = (
    "Band",
    "RowCol",
    "ValidPoints",
    "Average",
    "Median",
    "StdDev",
    "Minimum",
    "Maximum",
)

# These widths are extremely fragile, and if cubenorm changes,
# then these will need to be changed, too.
fieldwidth = dict()
for n in fieldnames:
    fieldwidth.setdefault(n, 15)
fieldwidth["Band"] = 8
fieldwidth["RowCol"] = 8


class Dialect(csv.Dialect):
    """A :class:`csv.Dialect` for the output of the ISIS
    ``cubenorm`` program."""

    delimiter = " "
    skipinitialspace = True
    quoting = csv.QUOTE_NONE
    escapechar = ""
    lineterminator = "\n"


class writer:
    """A class for writing out the fixed-width format required by ``cubenorm``.

    The interface is similar to the :class:`csv.writer` class, but does not
    inherit from it."""

    def __init__(self, f):
        self.file_object = f

    def writerow(self, row):
        line = ""
        for name, elem in zip(fieldnames, row):
            right_aligned = "{:>" + str(fieldwidth[name]) + "}"
            line += right_aligned.format(elem)

        self.file_object.write(line + "\n")

    def writerows(self, rows):
        for r in rows:
            self.writerow(r)

    def writeheader(self):
        """A convenience function, since the fieldnames are pre-defined."""
        self.writerow(fieldnames)


class DictWriter(csv.DictWriter):
    """A DictWriter for ``cubenorm`` files."""

    def __init__(
        self,
        f,
        restval="",
        extrasaction="raise",
        dialect=Dialect,
        *args,
        **kwds
    ):
        self.fieldnames = fieldnames
        self.restval = restval
        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError(
                f"extrasaction ({extrasaction}) must be 'raise' or 'ignore'"
            )
        self.extrasaction = extrasaction
        self.writer = writer(f)
