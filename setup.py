#! /usr/bin/env python3

from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()


setup(
    author='Beau Martinez',
    author_email='beau@beaumartinez.com',
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
    description='"What the FUCK did I do today?"',
    install_requires=[
        'requests>=2.2.1',
    ],
    licence='WTFPL',
    long_description=readme,
    name='standup',
    packages=find_packages(),
    scripts=[
        'bin/standup_codebase.py',
    ],
    url='http://github.com/beaumartinez/standup/',
    version='0.1',
)
