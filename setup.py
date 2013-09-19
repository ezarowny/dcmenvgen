#!/usr/bin/env python

from distutils.core import setup

config = {
    'name': 'dcmenvgen',
    'version': '0.1',
    'description': 'Generates a DICOM environment',
    'author': 'Eric Zarowny',
    'author_email': 'ezarowny@gmail.com',
    'url': 'https://github.com/ezarowny/dcmenvgen',
    'packages': ['dcmenvgen'],
    'scripts': ['scripts/dcmenvgen'],
}

setup(**config)
