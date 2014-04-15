#! /usr/bin/env python3

from distutils.core import setup


setup(
    author='Beau Martinez',
    description='What the FUCK did I do today',
    name='standup',
    packages=['standup', 'standup.codebase'],
    scripts=['bin/standup_codebase.py'],
    url='http://github.com/beaumartinez/standup/',
    version='0.1',
)
