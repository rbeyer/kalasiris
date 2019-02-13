#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sets up persistent resources for testing."""

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

import os, shutil, urllib.request

tdir = 'tests'
rdir = os.path.join(tdir, 'resources')
test_img = os.path.join( rdir, 'HiRISE_test.img' )

if not os.path.isdir( rdir ):
    os.mkdir( rdir )

if not os.path.isfile( test_img ):
    print( 'Downloading test HiRISE EDR image.' )
    urllib.request.urlretrieve( 'https://hirise-pds.lpl.arizona.edu/PDS/EDR/PSP/ORB_010500_010599/PSP_010502_2090/PSP_010502_2090_RED5_0.IMG', test_img )

