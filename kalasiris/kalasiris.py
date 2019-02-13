#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains calls to ISIS functions."""

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
import os, subprocess, sys
# This file shall have *NO* external dependencies.

# These definitions and the use of env= in the subprocess.run calls allow us to
# run ISIS in a very lean environment.  Of course, users can override with
# their complete environment by making kalasiris.environ = os.environ
# before any calls to ISIS programs.
#
# If you uncomment the two double-hash (##) lines, and comment out the two
# lines that get those values directly os.environ, you can run ISIS programs
# even though the shell that called this Python program may not be an
# ISIS-enabled shell.
## _isisroot =  os.path.join( os.environ['HOME'], 'anaconda3', 'envs', 'isis3' )
## _isis3data = os.path.join( os.environ['HOME'], 'anaconda3', 'envs', 'data' )
_isisroot =  os.environ['ISISROOT']
_isis3data = os.environ['ISIS3DATA']
environ = {'ISISROOT':  _isisroot,
          'ISIS3DATA': _isis3data,
          'PATH':      os.path.join(_isisroot, 'bin'),
          'HOME':      os.environ['HOME']} # Otherwise ISIS tries to make a ./\$HOME dir

#########################################################################
# Helper and wrapper functions for the ISIS commands.

def param_fmt(key: str, value: str)-> str:
    '''Returns a "key=value" string from the inputs.

    This is the pattern that ISIS uses for arguments.  If there are
    any trailing underbars (_) on the key, they will be stripped
    off.  This supports the old Pysis syntax to protect Python
    reserved words like from and min, while still allowing the user
    to provide 'natural' function calls like isis.stats(from_=cubefile)
    '''
    return '{}={}'.format(key.rstrip('_'), value)

def _run_isis_program( cmd: list )-> subprocess.CompletedProcess:
    '''Wrapper for subprocess.run()'''
    return subprocess.run(cmd, env=environ, check=True,
			  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			  universal_newlines=True)


def _build_isis_fn( fn_name: str ):
    '''This automatically builds a simple function to call an ISIS program.'''

    # Define the structure of the generic function, isis_fn:
    def isis_fn( *args, **kwargs )-> subprocess.CompletedProcess:
        if len(args) > 1: raise IndexError('only accepts 1 non-keyword argument to be from= ')
        cmd = [fn_name]
        if len(args) == 1: cmd.append( param_fmt('from', args[0]) )
        cmd.extend( map(param_fmt, kwargs.keys(), kwargs.values()) )
        return( _run_isis_program(cmd) )
    isis_fn.__name__ = fn_name
    isis_fn.__doc__ = f'Runs ISIS3 {fn_name}'

    # Then add it, by name to the enclosing module.
    setattr( sys.modules[__name__], fn_name, isis_fn)
    # Could have also used sys.modules['kalasiris'] if I wanted to be explicit.

# def _get_isis_program_names()-> iterable:
#     '''Returns an iterable of ISIS program names.
#
#     With the new conda distribution, there is a lot of stuff in $ISISROOT/bin
#     that isn't actually an ISIS program.  It would be nice if there was some
#     smart, automatic way to just get ISIS program names, but at the moment,
#     we just slurp up all the names in $ISISROOT/bin and make functions for them.
#
#     So somebody could try and run isis.python( 'my.py' ), but it would end up
#     calling 'python from=my.py' in the shell which would error, but the possibility
#     for mischeif exists.
#
#     This also means that the list this function returns is almost a thousand elements
#     long.  And while you can
#     import kalasiris as isis
#     programs are strongly encouraged limit what they import
#     from kalasiris import cam2map, hist
#     '''
#     bindir = os.path.join(environ['ISISROOT'],'bin')
#     with os.scandir( bindir ) as it:
#         for entry in it:
#             if entry.is_file() and os.access(entry, os.X_OK):
#                 yield entry.name


# Now use the builder function to automatically create functions with these names:
_isis_programs = ['crop','cubenorm','handmos','hist','histat','mask','stats']

# Could also reach out and grab these names from the $ISISROOT/bin/ directory.
for p in _isis_programs:
    _build_isis_fn( p )


# Explicit calls to ISIS programs below here, alphabetically arranged.
# These we want to be able to call or return differently than _build_isis_fn() provides.

def fx( **kwargs ):
    '''Runs ISIS3 getkey'''
    # Feature unlike *most* ISIS programs, there is no from= argument for fx
    cmd = ['fx']
    cmd.extend( map(param_fmt, kwargs.keys(), kwargs.values()) )
    return( _run_isis_program(cmd) )

def getkey(cube, grpname, keyword):
    '''Runs ISIS3 getkey'''
    # Feature: Simplified calling (no params), and returns a string
    #          instead of a subprocess.CompletedProcess
    cmd = ['getkey', 'from='+cube, 'grpname='+grpname, 'keyword='+keyword]
    return( _run_isis_program( cmd ).stdout.strip() )

def hi2isis(img, to=None, **kwargs):
    '''Runs ISIS3 hi2isis'''
    # Feature: If an argument for to= isn't provided, create a sensible default.
    if to is None:
        to = os.path.splitext( img )[0] + '.cub'

    cmd = ['hi2isis', 'from='+img, 'to='+to]
    cmd.extend( map(param_fmt, kwargs.keys(), kwargs.values()) )
    return( _run_isis_program(cmd) )
