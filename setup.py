#! /usr/bin/env python3

from setuptools import setup


setup(
    author='Beau Martinez',
    author_email='beau@beaumartinez.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.4',
    ],
    description='What the FUCK did I do today',
    install_requires=[
        'requests>=2.2.1',
    ],
    name='standup',
    packages=[
        'standup',
        'standup.codebase',
    ],
    scripts=[
        'bin/standup_codebase.py',
    ],
    url='http://github.com/beaumartinez/standup/',
    version='0.1',
)
