#!/usr/bin/env python

import re

from codecs import open

from setuptools import setup

packages = [
    'jsonfeedvalidator',
]

requires = [
    "jsonschema",
]
test_requirements = ['pytest>=2.8.0', "requests"]

with open('jsonfeedvalidator/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='jsonfeedvalidator',
    version=version,
    description='A JSON feed validator',
    long_description=readme,
    author='Alex Kessinger',
    author_email='voidfiles@gmail.com',
    url="https://github.com/voidfiles/jsonfeedvalidator",
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'jsonfeedvalidator': 'jsonfeedvalidator'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    tests_require=test_requirements,
)
