#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'bricks_occupant',
]

setup(
    name='bricks_occupant',
    description='Bricks guest agent',
    long_description='',
    author='Cloud A',
    author_email='info@clouda.ca',
    url='https://bitbucket.org/clouda/bricks-occupant',
    packages=packages,
    scripts=['bin/bricks_occupant'],
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
