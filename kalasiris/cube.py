#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""These functions provide some mechanisms for dealing with
ISIS cube files.  These functions are not comprehensive, and only
seek to provide functionality that does not exist elsewhere.

For example, there is already a GDAL driver for ISIS cubes, and
access to the primary bands and such can already be accomplished
via GDAL, and in order to get the image pixels as a numpy array::

    import numpy as np
    from osgeo import gdal_array

    cube = 'some.cub'
    img_arr = gdal_array.LoadFile(cube)

If you want to make sure to mask out all of the special pixels
in the image you've read into img_arr above, you can do this::

    import pvl
    import kalasiris as isis

    label = pvl.load(cube)
    specialpix = getattr(isis.specialpixels,
                         label['IsisCube']['Core']['Pixels']['Type'])
    masked_img_arr = np.ma.masked_outside(img_arr,
                                          specialpix.Min, specialpix.Max)

"""

# Copyright 2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import os
import struct
from collections import abc
from typing import Tuple
from warnings import warn

import kalasiris as isis

data_sizes = {"Integer": 4, "Double": 8, "Real": 4, "Text": 1}
data_formats = {"Integer": "i", "Double": "d", "Real": "f"}


def _get_start_size(d: dict) -> Tuple[int, int]:
    """Returns a tuple of ints that represent the true start byte and size
    based on the provided dict.

    This is a convenience function such that if you have these values in a
    dictionary with a *StartByte* and *Bytes* keys.

    Since the StartByte labels on an ISIS cube are 1-based counts, and not
    0-based, in order to convert from the numbers provided in the labels
    to a byte count for Python's read() functions, you must subtract one
    from the listed StartByte, which this function does.
    """
    start = int(d["StartByte"]) - 1
    size = int(d["Bytes"])
    return start, size


def get_startsize_from(
    label=None, table_name=None, cube_path=None
) -> Tuple[int, int]:
    """Returns a tuple of ints that represent the true start byte and size
    based on the provided *label* or combination of *table_name* and
    *cube_path*.

    Either *label* or *table_name* and *cube_path* are needed.  If
    neither a *label* nor a *table_name* is provided, then this
    function will raise a ValueError.  If both are provided, *label*
    will take precedence and *table_name* will be ignored.

    *label* is a dict which must contain a *StartByte* key and a *Bytes*
    key whose values can be converted to int (if not already).  These
    values should be those in the cube file label for the table.

    The name of the table as a string can be provided via *table_name*
    and the ISIS getkey function will be applied to the file at
    *cube_path* to extract the needed StartByte and Bytes values
    from the label.  However, if there is more than one table in
    the cube, getkey can only find the first, and a ValueError might
    be returned.

    If the pvl library is available, this function will use it to find
    *all* of the tables in the *cube_path* labels and will find the one
    named by *table_name* if it is present.
    """
    if label is None and table_name is None:
        raise ValueError("Neither label nor table_name were provided.")

    if label is not None:
        return _get_start_size(label)
    else:
        try:
            import pvl

            label = pvl.load(str(cube_path))
            for t in label.getlist("Table"):
                if t["Name"] == table_name:
                    return _get_start_size(t)
            else:
                raise KeyError(
                    f"There is no table '{table_name}' in the "
                    f"labels of {cube_path}."
                )
        except ImportError:
            name = isis.getkey(
                cube_path, objname="Table", keyword="Name"
            ).stdout.strip()
            if table_name == name:
                return _get_start_size(
                    {
                        "StartByte": isis.getkey(
                            cube_path, objname="Table", keyword="StartByte"
                        ).stdout.strip(),
                        "Bytes": isis.getkey(
                            cube_path, objname="Table", keyword="Bytes"
                        ).stdout.strip(),
                    }
                )
            else:
                raise KeyError(
                    f"The first table in {cube_path} that ISIS getkey could "
                    f"find is not named {table_name} it is {name}.  If your "
                    "cube has more than one table, you can provide the info "
                    "via the label dict instead of table_name, or if you "
                    "install the pvl Python library then this function can "
                    "use it to find all of the tables."
                )


# This function is derived from this commit dated Sep 24, 2019:
# https://github.com/USGS-Astrogeology/ale/commit/add5368ba46b2c911de9515afeaccc4d1c981000
def read_table_data(
    cube_path: os.PathLike, label=None, table_name=None
) -> bytes:
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
    *all* of the tables in the *cube_path* labels and will find the one
    named by *table_name* if it is present.
    """

    (start, size) = get_startsize_from(label, table_name, cube_path)

    with open(cube_path, "rb") as cubehandle:
        cubehandle.seek(start)
        table = cubehandle.read(size)

    return table


# This function is derived from this commit dated Sep 24, 2019:
# https://github.com/USGS-Astrogeology/ale/commit/add5368ba46b2c911de9515afeaccc4d1c981000
def parse_table(data: bytes, fields: list) -> dict:
    """Return a Python dictionary created from the bytes *data* of
    an ISIS cube table (presumably extracted via read_table_data()),
    and described by the *fields* list and *records*.

    Please be aware that this does not perform masking of the ISIS
    special pixels that may be present in the table, and simply
    returns them as the appropriate int or float values.

    The *fields* list must be a list of dicts, each of which must
    contain the following keys: 'Name', 'Type', and 'Size'.  The
    'Name' key can be any string (and these will end up being the
    keys in the returned dict).  'Size' is the size in bytes of the
    field, and 'Type' is a string that must be one of 'Integer',
    'Double', 'Real', or 'Text'.

    If you are using the pvl library, the get_table() function will
    be easier to use.
    """

    row_len = 0
    for f in fields:
        row_len += data_sizes[f["Type"]] * int(f["Size"])
    if len(data) % row_len != 0:
        raise ValueError(
            f"The total sizes of each field ({row_len}) do not evenly divide "
            f"into the size of the data ({len(data)}), so something is off."
        )

    # Parse the binary data
    results = {f["Name"]: [] for f in fields}
    offset = 0
    while offset < len(data):
        for f in fields:
            if f["Type"] == "Text":
                field_data = data[offset : offset + int(f["Size"])].decode(
                    encoding="latin_1"
                )
            else:
                data_fmt = data_formats[f["Type"]] * int(f["Size"])
                f_data = struct.unpack_from(data_fmt, data, offset)
                if len(f_data) == 1:
                    field_data = f_data[0]
                else:
                    field_data = list(f_data)

            results[f["Name"]].append(field_data)
            offset += data_sizes[f["Type"]] * int(f["Size"])

    return results


# This function is derived from this commit dated Sep 24, 2019:
# https://github.com/USGS-Astrogeology/ale/commit/add5368ba46b2c911de9515afeaccc4d1c981000
def get_table(cube_path: os.PathLike, table_name: str) -> dict:
    """Return a Python dictionary created from the named table in the ISIS cube.

    This function requires the pvl Python library.
    """
    # Toyed with allowing a file_object=None argument, docstring would have
    # been:
    #
    # If the optional *file_object* is given, it should be the result
    # of opening *cube_path* which is readable.  This simply allows
    # a caller to provide an already-opened file object.  Otherwise,
    # this function will open and then close the file at *cube_path*.
    #
    # Decided against it, the potential to pass a file_object that was
    # *different* from an opened *cube_path* had the potential for much
    # mayhem without a tremendous amount of gain.

    try:
        import pvl

        label = pvl.load(str(cube_path))
        table_label = None
        for t in label.getlist("Table"):
            if t["Name"] == table_name:
                table_label = t
                break

        # if file_object is not None:
        #     (start, size) = _get_start_size(table_label)
        #     file_object.seek(start)
        #     table_data = file_object.read(size)
        # else:
        table_data = read_table_data(cube_path, table_label)
        return parse_table(table_data, table_label.getlist("Field"))

        # The original ale function added the keywords into the returned
        # table, but that doesn't seem like a great idea, since that means
        # that those keys are 'special' meta-data keys, whereas the other
        # keys in the returned dict are 'regular' field keys, and once
        # returned, there's no way to know which is which.
        # # Add the keywords from the label
        # results.update({
        #     key: value for key,
        #                    value in table_label.items() if not isinstance(
        #         value, pvl._collections.PVLGroup)})
        #
        # return results

    except ImportError:
        warn(
            "The pvl library is not present, so get_table() cannot be used. "
            "The parse_table() function might work for you.",
            ImportWarning,
        )
        raise


def overwrite_table_data(
    cube_path: os.PathLike, data: bytes, label=None, table_name=None
):
    """The file at *cube_path* will be modified by overwriting the
    data in the specfied table name with the contents of *data*.

    Either *label* or *table_name* is needed.  If neither a *label*
    dict (which must contain a 'Name' key) nor a *table_name* is
    provided, then this function will raise a ValueError.  If both
    are provided, *label* will take precedence and *table_name*
    will be ignored.

    *label* is a dict which must contain *Name*, *StartByte*, and
    *Bytes* keys (*StartByte* and *Bytes* must be convertable to
    int if not already).  These values will be used to locate where
    in the file to write the new *data*.

    The name of the table as a string can be provided via *table_name*
    and the ISIS getkey function will be applied to extract the needed
    StartByte and Bytes values from the label.  However, if there is more
    than one table in the cube, getkey can only find the first, and a
    ValueError might be returned, even thought there is a table of that
    name in the file.

    If the pvl library is available, this function will use it to find
    *all* of the tables in the *cube_path* labels and will find the one
    named by *table_name* if it is present.
    """

    (start, size) = get_startsize_from(label, table_name, cube_path)

    if size != len(data):
        raise ValueError(
            f"The size of the table ({size}) to be overwritten from the file "
            f"({cube_path}) is different from size of the data provided "
            f"({len(data)})."
        )

    with open(cube_path, "r+b") as cubehandle:
        cubehandle.seek(start)
        cubehandle.write(data)

    return


def encode_table(table: dict, fields: list) -> bytes:
    """Return a bytes object created from the *table* dict.

    The *table* dict must contain lists of equal length as values.
    If they are not of equal length, an IndexError will be raised.

    The *fields* list must be a list of dicts, each of which must
    contain the following keys: 'Name', 'Type', and 'Size'.  The
    'Name' key can be any string, but must match the keys in the
    *table* dict.  'Size' is the size in bytes of the field, and
    'Type' is a string that must be one of 'Integer', 'Double',
    'Real', or 'Text'.

    If a field's 'Size' value is more than 1, then the list which
    is the value of the *table* with that key name must be a list of
    length 'Size'.

    If you are using the pvl library, the overwrite_table() function will
    be easier to use.
    """

    field_lengths = set()
    for v in table.values():
        field_lengths.add(len(v))

    if not len(field_lengths) == 1:
        raise IndexError(
            "At least one of the lists in the table has "
            f"a different length than the rest: {field_lengths}"
        )

    data = bytes()
    for row in range(field_lengths.pop()):
        for f in fields:
            obj = table[f["Name"]][row]
            size = int(f["Size"])
            if f["Type"] == "Text":
                if len(obj) > size:
                    raise IndexError(
                        f"The length of {obj} ({len(obj)}) is "
                        "larger than the allowable Size of the "
                        f"field ({size})"
                    )
                else:
                    data += obj.ljust(size).encode(encoding="latin_1")
            else:
                data_fmt = data_formats[f["Type"]] * size
                if isinstance(obj, abc.Sequence):
                    if len(obj) == size:
                        data += struct.pack(data_fmt, *obj)
                    else:
                        raise IndexError(
                            f"The length of {obj} ({len(obj)}) is different "
                            f"than the Size of the field ({size})."
                        )
                elif size == 1:
                    data += struct.pack(data_fmt, obj)
                else:
                    raise ValueError(
                        f"There is only a single value ({obj}) but the field "
                        f"indicates there should be {int(f['Size'])}."
                    )

    return data


def overwrite_table(cube_path: os.PathLike, table_name: str, table: dict):
    """The file at *cube_path* will be modified by overwriting the
    data in the specfied table name with the contents of *table*.

    The *table* dict must contain lists of equal length as values.
    If they are not of equal length, an IndexError will be raised.
    The *table* dict must also contain, as keys, all of the Field names
    from *table_name* in the *cube_path*.

    This function requires the pvl Python library.
    """

    try:
        import pvl

        label = pvl.load(str(cube_path))
        table_label = None
        for t in label.getlist("Table"):
            if t["Name"] == table_name:
                table_label = t
                break

        data = encode_table(table, table_label.getlist("Field"))
        overwrite_table_data(cube_path, data, table_label)

        return

    except ImportError:
        warn(
            "The pvl library is not present, so overwrite_table() cannot be "
            "used. The overwrite_table_data() function might work for you.",
            ImportWarning,
        )
        raise
