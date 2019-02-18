#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Makes the 'regular' ISIS functions act like the *_k functions*.

If you prefer the simplified argument structure and behavior of the
*_k functions*, but are constantly forgetting to put the ``_k`` on the end
of your function names, this module is for you.

For example, here's the 'regular' and *_k function* way of calling the ISIS
getkey program::

    import kalasiris as isis

    cube_file = 'some.cub'

    keyval = isis.getkey(cube_file, grpname='Instrument',
                         keyword='InstrumentId').stdout.strip()

    k_keyval = isis.getkey_k(cube_file, 'Instrument', 'InstrumentId')

And the values of ``keyval`` and ``k_keyval`` are the same.

However, if you do this::

    import kalasiris as isis

    cube_file = 'some.cub'

    key = isis.getkey(cube_file, 'Instrument', 'InstrumentId')

You'll get this exception::

    IndexError: only accepts 1 non-keyword argument to be from=

Because you tried to call ``isis.getkey()`` with the argument signature
of ``isis.getkey_k()`` and then ``isis.getkey()`` couldn't deal with it.

If you are always doing this, then instead of the above, do this::

    import kalasiris.sweetened as isis

    cube_file = 'some.cub'

    key = isis.getkey(cube_file, 'Instrument', 'InstrumentId')

And now the 'regularly' named functions will work the way that you expect the
*_k function* versions to act.
"""

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

from sys import modules

from .__init__ import *  # noqa F401,F403

from kalasiris import k_funcs

for k_func in dir(k_funcs):
    if k_func.endswith('_k'):
        reg_func = k_func.rsplit('_', maxsplit=1)[0]
        setattr(modules[__name__], reg_func, getattr(k_funcs, k_func))
