#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""These functions provide some mechanisms for dealing with
ISIS cube files.
"""

# Copyright 2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import os

from .kalasiris import getkey


def _get_start_size(d: dict) -> tuple(int, int):
    """Returns a tuple of ints that represent the true start byte and size
    based on the provided dict.

    This is a convenience function such that if you have these values in a
    dictionary with a *StartByte* and *Bytes* keys.

    Since the StartByte labels on an ISIS cube are 1-based counts, and not
    0-based, in order to convert from the numbers provided in the labels
    to a byte count for Python's read() functions, you must subtract one
    from the listed StartByte, which this function does.
    """
    start = int(d['StartByte']) - 1
    size = int(d['Bytes'])
    return (start, size)


# This function is derived from this commit dated Sep 24, 2019:
# https://github.com/USGS-Astrogeology/ale/commit/add5368ba46b2c911de9515afeaccc4d1c981000
def read_table_data(cube_path: os.PathLike,
                    label: None, table_name: None) -> bytes:
    """Returns a bytes object with the contents read from the file at
    *cube_path* based on the elements provided in the *label* or
    *table_name*.

    Either *label* or *table_name* is needed.  If neither a *label*
    nor a *table_name* is provided, then this function will raise
    a ValueError.  If both are provided, *label* will take precedence
    and *table_name* will be ignored.

    *label* is a dict which must contain a *StartByte* key and a *Bytes*
    key whose values can be converted to int (if not already).  These
    values should be those in the cube file label for the table.

    The name of the table as a string can be provided via *table_name*
    and the ISIS getkey function will be applied to extract the needed
    StartByte and Bytes values from the label.  However, if there is more
    than one table in the cube, getkey can only find the first, and a
    ValueError might be returned.

    If the pvl library is available, this function will use it to find
    *all* of the tables in the *cube_path* labels.
    """

    if label is None and table_name is None:
        raise ValueError("Neither label nor table_name were provided.")

    if label is not None:
        start, size = _get_start_size(label)
    else:
        try:
            import pvl
            label = pvl.load(cube_path)
            for t in label.getlist('Table'):
                if t['Name'] == table_name:
                    start, size = _get_start_size(t)
                    break
        except ImportError:
            name = getkey(cube_path, objname='Table', keyword='Name')
            if table_name == name:
                start, size = _get_start_size(
                    {'StartByte':
                     getkey(cube_path, objname='Table', keyword='StartByte'),
                     'Bytes':
                     getkey(cube_path, objname='Table', keyword='Bytes')})
            else:
                raise ValueError(f"The first table in {cube_path} that "
                                 "ISIS getkey could find is not named "
                                 f"{table_name} it is {name}.  If your "
                                 "cube has more than one table, you can "
                                 "provide the info via the label dict "
                                 "instead of table_name, or if you install "
                                 "the pvl Python library then this function "
                                 "can use it to find all of the tables.")

    cubehandle = open(cube, "rb")
    cubehandle.seek(start)
    return cubehandle.read(size)


# This function is derived from this commit dated Sep 24, 2019:
# https://github.com/USGS-Astrogeology/ale/commit/add5368ba46b2c911de9515afeaccc4d1c981000
def parse_table(data: bytes, fields: list) -> dict:
    """Return a Python dictionary created from the bytes *data* of
    an ISIS cube table (presumably extracted via read_table_data()),
    and described by the *fields* list and *records*.

    The *fields* list must be a list of dicts, each of which must
    contain the following keys: 'Name', 'Type', and 'Size'.  The
    'Name' key can be any string (and these will end up being the
    keys in the returned dict).  'Size' is the size in bytes of the
    field, and 'Type' is a string that must be one of 'Integer',
    'Double', 'Real', or 'Text'.

    The *records* count is also found in the table label.

    If you are using the pvl library, the get_table() function will
    be easier to use.
    """

    row_len = 0
    for f in fields:
        row_len += data_sizes[f['Type']] * f['Size']
    if len(data) % row_len != 0:
        raise ValueError(f"The total sizes of each field ({row_len}) do not "
                         "evenly divide into the size of the data "
                         f"({len(data)}), so something is off.")

    data_sizes = {'Integer': 4,
                  'Double': 8,
                  'Real': 4,
                  'Text': 1}
    data_formats = {'Integer': 'i',
                    'Double': 'd',
                    'Real': 'f'}

    # Parse the binary data
    results = {field['Name']: [] for field in fields}
    offset = 0
    while offset < len(data):
        for f in fields:
            if f['Type'] == 'Text':
                field_data = data[offset:offset + f['Size']].decode(
                    encoding='latin_1')
            else:
                data_fmt = data_formats[f['Type']] * f['Size']
                field_data = struct.unpack_from(data_fmt, data, offset)
                if len(field_data) == 1:
                    field_data = field_data[0]

            results[f['Name']].append(field_data)
            offset += data_sizes[f['Type']] * f['Size']

    return results


# This function is derived from this commit dated Sep 24, 2019:
# https://github.com/USGS-Astrogeology/ale/commit/add5368ba46b2c911de9515afeaccc4d1c981000
def get_table(cube_path: os.PathLike, table_name: str) -> dict:
    """Return a Python dictionary created from the named table in
    the ISIS cube.

    This function requires the pvl Python library.
    """

    try:
        import pvl
        label = pvl.load(cube_path)
        table_label = None
        for t in label.getlist('Table'):
            if t['Name'] == table_name:
                table_label = t
                break

        table_data = read_table_data(cube, table_label)
        results = parse_table(table_data, table_label.getlist('Field'))

        # Add the keywords from the label
        results.update({
            key: value for key, value in table_label.items() if not isinstance(
                value, pvl._collections.PVLGroup)})

        return results

    except ImportError:
        warn("The pvl library is not present, so get_table() cannot be used. "
             "The parse_table() function might work for you.", ImportWarning)
