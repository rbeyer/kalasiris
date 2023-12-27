=======
History
=======

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

When updating this file, please add an entry for your change under
Unreleased_ and one of the following headings:

- Added - for new features.
- Changed - for changes in existing functionality.
- Deprecated - for soon-to-be removed features.
- Removed - for now removed features.
- Fixed - for any bug fixes.
- Security - in case of vulnerabilities.

If the heading does not yet exist under Unreleased_, then add it
as a 3rd level heading, underlined with pluses (see examples below).

When preparing for a public release add a new 2nd level heading,
underlined with dashes under Unreleased_ with the version number
and the release date, in year-month-day format (see examples below).

Unreleased
----------


1.10.0 (2023-12-27)
-------------------

Added
+++++
* New kalasiris.set_persistent_preferences() functionality so that a library user can set
  a persistent preferences path rather than having to enter it with each kalasiris
  function run.  Addresses Issue #11.
* Can now also pass parameters that do not take an argument to ISIS in a manner similar
  to how you'd write them on the command line (e.g. `getkey("-help")`) in addition to
  the "old" way (e.g. `getkey("help__")`).


1.9.1 (2021-07-04)
------------------

Changed
+++++++
* Testing now defaults to only running on mocks.
* Consolidated boolean that controls testing on "real files" to single place.
* Enabled GitHub Workflows for testing.

Fixed
+++++
* Bug in reserved parameter handling, such that only some reserved parameters
  that were given with two trailing underbars (_) would be converted to their
  appropriate "-key=value" form for ISIS.  This was true for "restore" for example,
  which was embarrassingly given in the documentation, but not tested!
* PathSet module documentation was missing the first letters of several words.


1.9.0 (2020-10-13)
------------------

Added
+++++
* Now supports the new ISISDATA environment variable, in addition to ISIS3DATA.

1.8.0 (2020-06-01)
------------------
* Added the ability to pass arguments to ``subprocess.run()`` for each ISIS program.
* The ISIS functions now automatically log with a level of INFO.
* Adopted Conventional Commits pattern (https://www.conventionalcommits.org/en/v1.0.0) for commit messages.
* Adopted Black formatting.
* Minor spelling and formatting improvements.

1.7.1 (2020-05-05)
------------------
* Corrected a readthedocs failure.

1.7.0 (2020-05-05)
------------------
* Added some functions to read table data from cube files.
* Added special pixel values via specialpixels.py (implemented
  as namedtuples instead of as dictionaries, as in pysis).
* Enabled Python 3.7 and 3.8 tests for tox.

1.6.0 (2020-04-12)
------------------
* Provided pysis return type and exception emulation.
* Switched from Apache 2 to the BSD-3-Clause license.


1.5.0 (2019-11-16)
------------------
* Did some documentation formatting.
* Streamlined the fromlist module.
* Put in a protection from accidentally adding a Path to a PathSet twice.


1.4.0 (2019-10-08)
------------------
* Added the fromlist module.


1.3.0 (2019-10-06)
------------------
* Added the cubeit_k() k_function.
* Added TravisCI tests for ISIS 3.8.1 and 3.9.0
* Separated tests into those that can run in-memory with mocking, and those that
  need the filesystem, and ISIS, etc.


1.2.0 (2019-10-04)
------------------
* Added a documentation section to help guide a user to choose between pysis and kalasiris.
* Improved the documentation for the version module a little.
* Added the stats_k() k_function.


1.1.0 (2019-06-19)
------------------

* Added the version module in order to query and retrieve ISIS version
  information from the ISIS system.
* Added TravisCI tests for ISIS 3.7.1


1.0.0 (2019-04-24)
------------------

* Removed cubenormDialect, and moved it to cubenormfile.Dialect
* Implemented cubenormfile.writer and cubenormfile.DictWriter, to
  write the fixed-width file format that ISIS cubenorm will actually read.

0.2.0 (2019-03-23)
------------------

* Implemented a new feature: the PathSet Class.
* Enabled installation via ``conda-forge``
* Updated some documentation.
* Fixed it so that the module documentation appears in readthedocs

0.1.2 (2019-03-04)
------------------

* Discovered a bug that made us platform-dependent.  Fixed.
* Made a variety of documentation improvements.
* Enabled and tested install via ``pip install``
* Enabled testing via tox
* Enabled testing via Travis CI

0.1.1 (2019-02-22)
------------------

* Jesse discovered that the code was incorrectly testing for
  executability of the ``$ISISROOT/bin/xml/*xml`` files instead of
  the ``$ISISROOT/bin/*`` program files, and issued a PR that
  fixed it.


0.1.0 (2019-02-20)
------------------

* Initial creation finished. Time to share.

0.0.0 (2019-02-12)
------------------

* Started project.


Version Numbering
-----------------

The kalasiris library follows the `Semantic Versioning 2.0.0
specification <https://semver.org>`_, such that released kalasiris
version numbers follow this pattern: ``{major}.{minor}.{patch}``.
