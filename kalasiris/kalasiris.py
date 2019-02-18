#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides the ability to call ISIS functions."""

# Copyright 2019, Ross A. Beyer (rbeyer@seti.org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Thou shalt only import from the Python Standard Library.
import os
import subprocess
import sys
# This file shall have *NO* external dependencies.

# These definitions and the use of env= in the subprocess.run calls allow us to
# run ISIS in a very lean environment.  Of course, users can override with
# their complete environment by making kalasiris.environ = os.environ
# before any calls to ISIS programs.
_isisroot = os.environ['ISISROOT']
_isis3data = os.environ['ISIS3DATA']
environ = {'ISISROOT':  _isisroot,
           'ISIS3DATA': _isis3data,
           'PATH':      os.path.join(_isisroot, 'bin'),
           'HOME':      os.environ['HOME']}
# If we don't also set $HOME, ISIS tries to make a local ./\$HOME dir


def param_fmt(key: str, value: str) -> str:
    '''Returns a "key=value" string from the inputs.

    This is the pattern that ISIS uses for arguments.  If there are
    any trailing underbars (_) on the key, they will be stripped
    off.  This supports the old pysis syntax to protect Python
    reserved words like from and min, while still allowing the user
    to provide 'natural' function calls like isis.stats(from_=cubefile)
    '''
    return '{}={}'.format(key.rstrip('_'), value)


def _run_isis_program(cmd: list) -> subprocess.CompletedProcess:
    '''Wrapper for subprocess.run()'''
    return subprocess.run(cmd, env=environ, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True)


def _build_isis_fn(fn_name: str):
    '''This factory builds a simple function to call an ISIS program.'''

    # Define the structure of the generic function, isis_fn:
    def isis_fn(*args, **kwargs) -> subprocess.CompletedProcess:
        __name__ = fn_name
        __doc__ = f'Runs ISIS3 {fn_name}'
        if len(args) > 1:
            e = 'only accepts 1 non-keyword argument to be from= '
            raise IndexError(e)
        cmd = [fn_name]
        if len(args) == 1:
            cmd.append(param_fmt('from', args[0]))
        cmd.extend(map(param_fmt, kwargs.keys(), kwargs.values()))
        return(_run_isis_program(cmd))

    # Then add it, by name to the enclosing module.
    setattr(sys.modules[__name__], fn_name, isis_fn)
    # Could have also used sys.modules['kalasiris'] if I wanted to be explicit.


def _get_isis_program_names():
    '''Returns an iterable of ISIS program names.

    With the new conda distribution, there is a lot of stuff in
    $ISISROOT/bin that isn't actually an ISIS program.  So just
    slurping the names in $ISISROOT/bin gets too many things that
    aren't ISIS programs.

    Instead, the isis conda distribution provides $ISISROOT/bin/xml/
    which contains the documentation XML files.  Every XML file
    in that directory corresponds to the name of an ISIS program,
    which is perfect.
    '''
    # bindir = os.path.join(environ['ISISROOT'], 'bin')
    bindir = os.path.join(environ['ISISROOT'], 'bin', 'xml')
    with os.scandir(bindir) as it:
        for entry in it:
            if(entry.is_file()
               and os.access(entry, os.X_OK)
               and not entry.name.startswith('.')):
                (name, ext) = os.path.splitext(entry.name)
                if '.xml' == ext:
                    yield name


# Now use the builder function to automatically create functions
# with these names:
for p in _get_isis_program_names():
    _build_isis_fn(p)
