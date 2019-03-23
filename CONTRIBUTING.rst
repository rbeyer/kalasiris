.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/rbeyer/kalasiris/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

kalasiris could always use more documentation, whether as part of the
official kalasiris docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/rbeyer/kalasiris/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `kalasiris` for local development.

1. Fork the `kalasiris` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/kalasiris.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv kalasiris
    $ cd kalasiris/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

   *Suggestion*: If you are working a bugfix, write your tests first, and
   commit them in your branch, that way others can verify that the
   code is broken in the way you describe by looking at that first commit
   in your branch.

.. 5. When you're done making changes, check that your changes pass flake8 and the
..    tests, including testing other Python versions with tox::
..
..     $ flake8 kalasiris tests
..     $ python setup.py test or py.test
..     $ tox
..
..    To get flake8 and tox, just pip install them into your virtualenv.

5. When you're done making changes, check that your changes pass flake8 and the
   tests::

    $ make lint
    $ make test

   To get flake8, just pip install it into your virtualenv.

6. Now that it's working, add yourself to the list of Contributors
   in ``AUTHORS.rst`` if you aren't there already.  Please also
   consider adding your name to the Copyright line in any
   files you altered, if appropriate.

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6, and for PyPy.

..   Check
..   https://travis-ci.org/rbeyer/kalasiris/pull_requests
..   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::


    $ python -m unittest tests.test_kalasiris

Workflow and Deploying
----------------------

The workflow concept we use in the kalasiris project is as follows.
If you are familiar with Git workflows, it is mostly based on a
Gitflow model, but there is not a separate *develop* branch from
the *master* branch (at the moment, we don't need that much formalism),
so *master* is the development branch.

The kalasiris library follows the `Semantic Versioning 2.0.0
specification <https://semver.org>`_, such that released kalasiris
version numbers follow this pattern: ``{major}.{minor}.{patch}``.

In this section, as a shorthand for ``{major}.{minor}.{patch}``,
we will use *a.b.c*, but all actual versions in the repo will be
numeric.  When we talk about version *a.b.c*, consider those letters
as immutable variables that hold integers, and ``a += 1 == b, c +=
1 == d``, etc.  So *a.b.c* is some starting state, which could
represent *1.2.3*, then *a.b.d* would be *1.2.4* or *a.c.0* would
be *1.3.0*, etc.

Here is an example workflow for working on a bug that was discovered:

+------------------------------------------------+--------+-------+-----------+
| Bugfix Workflow                                | Branch | Tests | Version   |
+================================================+========+=======+===========+
| After the commit that releases a.b.c to master | master | pass  | a.b.c     |
| it should have been tagged va.b.c              |        |       |           |
+------------------------------------------------+--------+-------+-----------+
| **A software bug is discovered.**                                           |
+------------------------------------------------+--------+-------+-----------+
| Make a *hotfix* branch (could be an external   | hotfix |       |           |
| PR branch)                                     |        |       |           |
+------------------------------------------------+        +-------+           |
| First commit should be the 'failing tests'     |        | fail  |           |
| commit. Craft tests to verify the failure      |        |       |           |
| mode and commit the tests, without touching    |        |       |           |
| the main code.  This allows others to see      |        |       |           |
| exactly what the problems are.                 |        |       |           |
+------------------------------------------------+        |       |           |
| Make commits on *hotfix* to address issue      |        |       |           |
+------------------------------------------------+        +-------+           |
| Once tests pass, make a final commit, and it   |        | pass  |           |
| is ready for merging!                          |        |       |           |
+------------------------------------------------+--------+-------+-----------+
| External developers can now issue a pull request to get this merged into    |
| master.                                                                     |
|                                                                             |
| What follows is what internal developers do when a PR is received:          |
+------------------------------------------------+--------+-------+-----------+
| Checkout the proposed *hotfix* branch and      | hotfix |       |           |
| verify:                                        |        |       |           |
|                                                |        |       |           |
| 1. Are there tests that exercise the bug?      |        |       |           |
| 2. Does ``make lint`` pass?                    |        |       |           |
| 3. Does ``make test`` pass?                    |        |       |           |
| 4. Does ``make test-all`` pass?                |        |       |           |
| 5. Is it based on master?                      |        |       |           |
|                                                |        |       |           |
| Iterate with the submitter, if needed.         |        |       |           |
+------------------------------------------------+--------+-------+-----------+
| When satisfied with the above (no pushing until after the tag step):        |
+------------------------------------------------+--------+-------+-----------+
| Starting state: ``git checkout master``        | master | pass  | a.b.c     |
+------------------------------------------------+--------+       |           |
| ``git branch hotfix``                          | hotfix |       |           |
|                                                |        |       |           |
| Checkout hotfix, may need to                   |        |       |           |
| ``git rebase master`` if master has advanced.  |        |       |           |
+------------------------------------------------+        |       +-----------+
| Commit with bump2version::                     |        |       | a.b.d-dev |
|                                                |        |       |           |
|   bump2version patch                           |        |       |           |
+------------------------------------------------+        +-------+           |
| Is there a suitable first `failing-tests`      |        | fail  |           |
| commit?  If not, decide how important it is.   |        | in    |           |
| If it is important to have those failing tests |        | the   |           |
| as the first item in the commit history, then  |        | first |           |
| you'll have to do some commit surgery with     |        | commit|           |
| ``git rebase -i`` and other things to arrange  |        |       |           |
| that.                                          |        |       |           |
+------------------------------------------------+        +-------+           |
| * If there are any new external developers:    |        | pass  |           |
|   add to ``AUTHORS.rst`` (if they haven't)     |        |       |           |
| * Edit ``HISTORY.rst`` to describe what        |        |       |           |
|   happened by reviewing commit messages.       |        |       |           |
| * If there are any commits in master since     |        |       |           |
|   the last release, include them in the        |        |       |           |
|   ``HISTORY.rst`` file, too.                   |        |       |           |
| * Otherwise check that everything is ready     |        |       |           |
|   to be merged back into master, and perform   |        |       |           |
|   a final pre-bump commit.                     |        |       |           |
+------------------------------------------------+        |       |           |
| Tidy commits with ``git rebase -i master``     |        |       |           |
| so that the commit history looks like this     |        |       |           |
| (most recent last):                            |        |       |           |
|                                                |        |       |           |
| #. Found a bug, these tests show what's wrong  |        |       |           |
| #. Bump version: a.b.c → a.b.d-dev             |        |       |           |
| #. Fixed the bug by doing x, y, and z          |        |       |           |
|                                                |        |       |           |
| Additional commits are fine, but any final     |        |       |           |
| ``HISTORY.rst`` or ``AUTHORS.rst`` changes     |        |       |           |
| should probably be squashed into the last      |        |       |           |
| commit.                                        |        |       |           |
+------------------------------------------------+        |       +-----------+
| This wraps up this branch and readies it for   |        |       | a.b.d     |
| merging with master::                          |        |       |           |
|                                                |        |       |           |
|  bump2version release --tag                    |        |       |           |
|     --tag-message                              |        |       |           |
|     'something descriptive'                    |        |       |           |
+------------------------------------------------+--------+       |           |
| apply to master::                              | master |       |           |
|                                                |        |       |           |
|   git checkout master                          |        |       |           |
|   git merge hotfix                             |        |       |           |
+------------------------------------------------+        |       |           |
| ::                                             |        |       |           |
|                                                |        |       |           |
|  git push                                      |        |       |           |
|  git push --tags                               |        |       |           |
+------------------------------------------------+--------+-------+-----------+
| The topic branch can now be deleted::                                       |
|                                                                             |
|   git branch -d hotfix                                                      |
+-----------------------------------------------------------------------------+
| Push new release to PyPI::                                                  |
|                                                                             |
|   make release                                                              |
+-----------------------------------------------------------------------------+
| Update the `conda-forge feedstock                                           |
| <https://github.com/conda-forge/kalasiris-feedstock>`_                      |
|                                                                             |
| Basically just follow the directions at the bottom of the feedstock repo:   |
|                                                                             |
| #. Fork the feestock repo                                                   |
| #. Update the ``recipe/meta.yml`` file                                      |
| #. Submit PR                                                                |
+-----------------------------------------------------------------------------+

The workflow for a minor feature is identical to the above, but we
might name the branch *feature* or *minor-feature* instead of
*hotfix*, and we would apply ``bump2version`` differently.

A **Minor Feature** is defined as new, backwards compatible functionality.

+------------------------------------------------+---------+-------+-----------+
| Minor Feature Workflow (differences from above)| Branch  | Tests | Version   |
+================================================+=========+=======+===========+
| After release a.b.c, the state is:             | master  | pass  | a.b.c     |
+------------------------------------------------+---------+       +-----------+
| 1st bump2version: ``bump2version minor``       | feature |       | a.c.0-dev |
+------------------------------------------------+         +-------+           +
| In this case, commits might look like this:    |         | fail  |           |
|                                                |         |       |           |
| #. Bump version: a.b.c → a.c.0-dev             |         |       |           |
| #. Working on a new feature                    |         |       |           |
| #. Wrote some tests                            |         |       |           |
| #. Feature is now complete!                    |         |       |           |
+------------------------------------------------+         +-------+-----------+
| 2nd bump2version::                             |         | pass  | a.c.0     |
|                                                |         |       |           |
|   bump2version release                         |         |       |           |
|     --tag --tag-message '...'                  |         |       |           |
+------------------------------------------------+---------+-------+-----------+

A **Major Feature** consists of backwards incompatible changes, and its workflow is
similar to the Minor Feature Workflow above, simply:

+------------------------------------------------+---------+-------+-----------+
| Major Feature Workflow (differences from above)| Branch  | Tests | Version   |
+================================================+=========+=======+===========+
| After release a.b.c, the state is:             | master  | pass  | a.b.c     |
+------------------------------------------------+---------+       +-----------+
| 1st bump2version: ``bump2version major``       | feature |       | b.0.0-dev |
+------------------------------------------------+         +-------+-----------+
| 2nd bump2version                               |         | pass  | b.0.0     |
+------------------------------------------------+---------+-------+-----------+


.. Deploying
.. ---------
..
.. A reminder for the maintainers on how to deploy.
.. Make sure all your changes are committed (including an entry in HISTORY.rst).
.. Then run::
..
.. $ bump2version release # possibly: major / minor / patch
.. $ git push
.. $ git push --tags
..
.. Travis will then deploy to PyPI if tests pass.
