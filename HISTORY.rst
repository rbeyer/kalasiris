=======
History
=======

0.1.0 (2019-02-??)
------------------


0.0.0 (2019-02-12)
------------------

* Started project.


Version Numbering
-----------------

The kalasiris library follows the `Semantic Versioning 2.0.0
specification <https://semver.org>`_, such that released kalasiris
version numbers follow this pattern: ``{major}.{minor}.{patch}``.

If you look at code in the repo, you'll see that it most likely has
a *dev* pre-release identifier, and the version number follows this
pattern: ``{major}.{minor}.{patch}-dev``.  Such that after we release
version ``a.b.c``, we will bump the version to typically be
``a.c.0-dev`` if we are working on new features, and work will
continue.  If bugs are discovered in ``a.b.c``, we will work on a
bug-fix branch, release ``a.b.d``, and merge it into ``a.c.0-dev``.
When we're happy with the state of ``a.c.0-dev``, it will be released
as ``a.c.0``, etc.
