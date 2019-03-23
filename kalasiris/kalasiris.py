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
from pathlib import Path
# This file shall have *NO* non-Standard Library dependencies.

# kalasiris library version:
__version__ = '0.2.0'

# These definitions and the use of env= in the subprocess.run calls allow us to
# run ISIS in a very lean environment.  Of course, users can override with
# their complete environment by making kalasiris.environ = os.environ
# before any calls to ISIS programs.
_isisroot = os.environ['ISISROOT']
_isis3data = os.environ['ISIS3DATA']
environ = {'ISISROOT':  _isisroot,
           'ISIS3DATA': _isis3data,
           'PATH':      str(Path(_isisroot) / 'bin'),
           'HOME':      os.path.expanduser('~')}
# If we don't also set $HOME, ISIS tries to make a local ./\$HOME dir
# Can't just use os.environ['HOME'] because not all platforms have
# that environment variable set (Windows uses something different).

# These are the names of the reserved parameters that can be given
# as arguments to any ISIS program, prefixed by a dash (-).
_res_param_no_vals = set(['webhelp', 'last', 'gui', 'nogui', 'verbose'])
_res_param_maybe = set(['help', 'log', 'info', 'save'])

# The ISIS programs in this list do not follow the 'normal' argument
# patters for most ISIS programs, they just consume everything you
# give them, so we need to treat them differently.
_pass_through_programs = set(['cneteditor', 'qmos', 'qnet', 'qtie', 'qview'])


def param_fmt(key: str, value: str) -> str:
    '''Returns a "key=value" string from the inputs.

    This is the pattern that ISIS uses for arguments.  If there are
    any trailing underbars (_) on the key, they will be stripped
    off.  This supports the old pysis syntax to protect Python
    reserved words like from and min, while still allowing the user
    to provide 'natural' function calls like isis.stats(from_=cubefile).

    Additionally, it also supports passing what ISIS calls *reserved
    parameters* for any ISIS program, denoted with a prefix of a single
    dash, like ``-restore=file`` or ``-verbose`` via keys with two trailing
    underbars.  So to call ``spiceinit from= some.cub -restore=file`` you
    would do this::

        cubefile = 'some.cub'
        restore_file = 'some.par'
        isis.spiceinit(cubefile, restore__=restore_file)

    Likewise, to call ``getkey -help``, or ``getkey -help=GRPNAME`` do this::

        isis.getkey('help__')
        isis.getkey(help__='GRPNAME')

    Of course, you'll probably want to do this::

        help_text = isis.getkey(help__='').stdout
    '''
    # The logic for dealing with a single parameter, like
    # isis.getkey('help__') # is down in the _build_isis_fn() factory
    # method.
    if key.endswith('__') and key.rstrip('_') in _res_param_maybe:
        return '-{}={}'.format(key.rstrip('_'), value)
    else:
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
        __name__ = fn_name                 # noqa: F841
        __doc__ = f'Runs ISIS3 {fn_name}'  # noqa: F841
        cmd = [fn_name]
        if fn_name in _pass_through_programs:
            cmd.extend(args)
        else:
            args_list = list(args)
            if len(args) > 0 and not str(args[0]).endswith('__'):
                cmd.append(param_fmt('from', args_list.pop(0)))
            for a in args_list:
                if a.endswith('__') and a.rstrip('_') in \
                        _res_param_no_vals.union(_res_param_maybe):
                    cmd.append('-{}'.format(a.rstrip('_')))
                else:
                    e = ('only accepts 1 non-keyword argument '
                         '(and sets it to from= ) '
                         'not sure what to do with ' + a)
                    raise IndexError(e)
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
    bindir = Path(environ['ISISROOT']) / 'bin'
    xmldir = bindir / 'xml'
    for entry in xmldir.iterdir():
        if(entry.is_file() and
           (bindir / entry.stem).is_file() and
           os.access(bindir / entry.stem, os.X_OK) and
           not entry.name.startswith('.')):
            if '.xml' == entry.suffix:
                yield entry.stem


# Now use the builder function to automatically create functions
# with these names:
for p in _get_isis_program_names():
    _build_isis_fn(p)
