# -*- coding: utf-8 -*-

"""Constants for Isis Special Pixels.

The constants are provided as SpecialPixel :func:collection.namedtuple:
objects, and have the following keys: Min, Null, Lrs, Lis, His,
Hrs, and Max.

Null
    A null pixel indicates no data was collected at the particular
    location.

Lis
    A low instrument saturation pixel occurred meaning the
    instrument readout was at its lowest possible value.

His
    A high instrument saturation pixel occurred meaning the
    instrument readout was at its highest possible value.

Lrs
    A low representation saturation pixel occurred meaning a
    program computed a new pixel value at this location that
    was lower than native bit-type for the file (e.g., less
    than zero for an 8-bit file).

Hrs:
    A high representation saturation pixel occurred meaning a
    program computed a new pixel value at this location that
    was greater than native bit-type for the file (e.g., greater
    than 255 for an 8-bit file).

The above definitions come from the `Logical Cube Format Guide
<https://isis.astrogeology.usgs.gov/documents/LogicalCubeFormatGuide/LogicalCubeFormatGuide.html>`_
and the numerical values come from the ISIS `SpecialPixel.h
<https://github.com/USGS-Astrogeology/ISIS3/blob/dev/isis/src/base/objs/SpecialPixel/SpecialPixel.h>`_ file.

In order to be able to know whether value should result in a
*Lrs* or *Hrs* value, we must also know:

Min
    The minimum valid value for a pixel.

Max
    The maximum valid value for a pixel.
"""  # noqa

# Copyright 2015, William Trevor Olson
# Copyright 2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import collections
import struct
import sys


SpecialPixels = collections.namedtuple(
    "SpecialPixels", ["Min", "Null", "Lrs", "Lis", "His", "Hrs", "Max"]
)

# 1-byte special pixel values from SpecialPixel.h
UnsignedByte = SpecialPixels(
    Min=1, Null=0, Lrs=0, Lis=0, His=255, Hrs=255, Max=254
)

# 2-byte unsigned special pixel values from SpecialPixel.h
UnsignedWord = SpecialPixels(
    Min=3, Null=0, Lrs=1, Lis=2, His=65534, Hrs=65535, Max=65522
)

# 2-byte signed special pixel values from SpecialPixel.h
SignedWord = SpecialPixels(
    Min=-32752,
    Null=-32768,
    Lrs=-32767,
    Lis=-32766,
    His=-32765,
    Hrs=-32764,
    Max=32767,
)

# 4-byte unsigned special pixel values from SpecialPixel.h
# This deals with unsigned long int values.  Not sure why there
# is so much space between 'Max' and the 'His' and 'Hrs' values, but
# that's what's in SpecialPixel.h.
UnsignedInteger = SpecialPixels(
    Min=3, Null=0, Lrs=1, Lis=2, His=4294967294, Hrs=4294967295, Max=4294967282
)

# This was in the original pysis, but I don't see it in SpecialPixel.h?
# The 'Max' value indicates that it is like a long int, but the 'Min'
# and other negative values are far from the possible representation
# minimum of a long int, so not sure what's going on here.
SignedInteger = SpecialPixels(
    Min=-8388614,
    Null=-8388613,
    Lrs=-8388612,
    Lis=-8388611,
    His=-8388610,
    Hrs=-8388609,
    Max=2147483647,
)

# 4-byte special pixel values for IEEE floating point from SpecialPixel.h
Real = SpecialPixels(
    Min=struct.unpack(">f", bytes.fromhex("FF7FFFFA"))[0],
    Null=struct.unpack(">f", bytes.fromhex("FF7FFFFB"))[0],
    Lrs=struct.unpack(">f", bytes.fromhex("FF7FFFFC"))[0],
    Lis=struct.unpack(">f", bytes.fromhex("FF7FFFFD"))[0],
    His=struct.unpack(">f", bytes.fromhex("FF7FFFFE"))[0],
    Hrs=struct.unpack(">f", bytes.fromhex("FF7FFFFF"))[0],
    Max=sys.float_info.max,
)

# 8-byte special pixel values for IEEE floating point from SpecialPixel.h
Double = SpecialPixels(
    Min=struct.unpack(">d", bytes.fromhex("FFEFFFFF FFFFFFFA"))[0],
    Null=struct.unpack(">d", bytes.fromhex("FFEFFFFF FFFFFFFB"))[0],
    Lrs=struct.unpack(">d", bytes.fromhex("FFEFFFFF FFFFFFFC"))[0],
    Lis=struct.unpack(">d", bytes.fromhex("FFEFFFFF FFFFFFFD"))[0],
    His=struct.unpack(">d", bytes.fromhex("FFEFFFFF FFFFFFFE"))[0],
    Hrs=struct.unpack(">d", bytes.fromhex("FFEFFFFF FFFFFFFF"))[0],
    Max=sys.float_info.max,
)
