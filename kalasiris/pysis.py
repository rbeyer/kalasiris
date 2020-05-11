#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Makes the 'regular' ISIS functions return what pysis did.

If you have old code that was built with pysis and is doing this::

    from pysis import isis

    value = isis.getkey(from_='W1467351325_4.map.cal.cub',
                        keyword='minimumringradius',
                        grp='mapping')

And you want to start using kalasiris, but don't want to overhaul
a bunch of code, you can just change the import line like so::

    import kalasiris.pysis as isis

    value = isis.getkey(from_='W1467351325_4.map.cal.cub',
                        keyword='minimumringradius',
                        grp='mapping')

And you should be good to go.  Note that this works for calls to
ISIS programs, but does not provide the pysis IsisPool functionality,
nor any of the non-ISIS pysis functions or classes, like ``pysis.cubefile``,
``pysis.specialpixels``, etc.
"""

# Copyright 2015, William Trevor Olson
# Copyright 2020, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import subprocess
import sys

import kalasiris as kala
from .kalasiris import _get_isis_program_names as gipn


class IsisException(Exception):
    """Base exception for pysis errors."""


class ProcessError(IsisException):
    """This exception is raised when an ISIS process returns a non-zero
    exit status."""

    def __init__(self, returncode, cmd, stdout, stderr):
        self.returncode = returncode
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr

        msg = (
            f"Command {self.cmd} returned non-zero exit "
            f"status {self.returncode}."
        )
        super(ProcessError, self).__init__(msg)


def _build_pysis_fn(fn_name: str):
    """This factory builds a simple function call to wrap
    kalasiris function calls for pysis return types and
    pysis Exception types."""

    # Define the structure:
    def pysis_fn(*args, **kwargs):
        __name__ = fn_name  # noqa: F841
        __doc__ = f"Runs ISIS {fn_name}"  # noqa: F841

        try:
            kala_fn = getattr(kala, fn_name)
            return kala_fn(*args, **kwargs).stdout.encode()
        except subprocess.CalledProcessError as err:
            raise ProcessError(err.returncode, err.cmd, err.stdout, err.stderr)

    # Then add it by name to the enclosing module, pysis.
    setattr(sys.modules[__name__], fn_name, pysis_fn)


for p in gipn():
    _build_pysis_fn(p)
