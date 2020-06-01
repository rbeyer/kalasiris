#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Ross A. Beyer",
    author_email='rbeyer@seti.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A Python library to wrap functions and functionality for the Integrated Software for Imagers and Spectrometers (ISIS).",
    install_requires=requirements,
    license="BSD-3-Clause License",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kalasiris',
    name='kalasiris',
    packages=find_packages(include=['kalasiris']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbeyer/kalasiris',
    version='1.8.0',
    zip_safe=False,
)
