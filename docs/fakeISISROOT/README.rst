============
fakeISISROOT
============

In order to build the docs without downloading ISIS (which isn't
really needed), we just need to have this ``fakeISISROOT``, with a
``bin/xml/`` directory full of *prog_name.xml* files.  It can be
built with ``make fakeISISROOT-docs`` in the top-level project
directory, *not* the ``docs/`` directory above.
