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

import os, subprocess, sys

# These definitions and the use of env= in the subprocess.run calls allow us to
# run ISIS in a very lean environment.
#
# If you uncomment the four double-hash (##) lines, and comment out the two
# lines that pull from os.environ, you can run ISIS programs even though the
# shell that called this Python program may not be an ISIS-enabled shell.
## isisroot = '/Users/rbeyer/anaconda3/envs/isis3'
## isis3data = '/Users/rbeyer/anaconda3/envs/isis3/data'
## isis_env = {'ISISROOT': isisroot,
##             'ISIS3DATA': isis3data,
isis_env = {'ISISROOT': os.environ['ISISROOT'],
            'ISIS3DATA': os.environ['ISIS3DATA'],
            'PATH': isisroot+'/bin/',
            'HOME': os.environ['HOME']} # Otherwise ISIS tries to make a ./\$HOME dir

#########################################################################
# Helper and wrapper functions for the ISIS commands.

def addparams( cmd, params ):
    '''Builds a list of strings from dictionary keys and values where the elements are "key=value".'''
    if params:
        for name in params:
            cmd.append( f'{name}={params[name]}' )
    return cmd

def _run_isis_program( cmd ):
    '''Wrapper for subprocess.run()'''
    return subprocess.run(cmd, env=isis_env, check=True, capture_output=True, text=True)


def _build_isis_fn( fn_name ):
    '''This automatically builds a simple function to call an ISIS program, based on the name given.'''
    # Define the structure of the generic function, fn:
    def isis_fn( fromcube, **keywords ):
        cmd = [fn_name, 'from='+fromcube]
        return( _run_isis_program( addparams(cmd, keywords) ) )
    isis_fn.__name__ = fn_name
    isis_fn.__doc__ = f'Runs ISIS3 {fn_name}'

    # Then add it, by name to the enclosing module.
    setattr( sys.modules[__name__], fn_name, isis_fn)
    # Could have also used sys.modules['isis'] if I wanted to be explicit.

# Now use the builder function to automatically create functions with these names:
_isis_programs = ['crop','cubenorm','handmos','hist','histat','mask','stats']
# Could also reach out and grab these names from the $ISISROOT/bin/ directory.
for p in _isis_programs:
    _build_isis_fn( p )


# Explicit calls to ISIS programs below here, alphabetically arranged.
# These we want to be able to call or return differently than _build_isis_fn() provides.

def fx( **keywords ):
    '''Runs ISIS3 getkey'''
    # Feature unlike *most* ISIS programs, there is no from= argument for fx
    cmd = ['fx']
    return( _run_isis_program( addparams(cmd, keywords) ) )

def getkey(cube, grpname, keyword):
    '''Runs ISIS3 getkey'''
    # Feature: Simplified calling (no params), and returns a string
    #          instead of a subprocess.CompletedProcess
    cmd = ['getkey', 'from='+cube, 'grpname='+grpname, 'keyword='+keyword]
    return( _run_isis_program( cmd ).stdout.strip() )

def hi2isis(img, to=None, **keywords):
    '''Runs ISIS3 hi2isis'''
    # Feature: If an argument for to= isn't provided, create a sensible default.
    if to is None:
        to = os.path.splitext( img )[0] + '.cub'

    cmd = ['hi2isis', 'from='+img, 'to='+to]
    return( _run_isis_program( addparams(cmd, keywords) ) )
