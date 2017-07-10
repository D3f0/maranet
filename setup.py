#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'twisted',
    'construct<=2.5.0',

]

setup_requirements = [
    'pytest-runner',
    # TODO(D3f0): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='maranet',
    version='1.0.1',
    description="A Python client library for MARA protocol. Includes server emulator, although MARA servers are tipically microcontrollers.",
    long_description=readme + '\n\n' + history,
    author="Nahuel Defossé",
    author_email='ndefosse@tw.unp.edu.ar',
    url='https://github.com/D3f0/maranet',
    packages=find_packages(include=['maranet']),
    entry_points={
        'console_scripts': [
            'maranet=maranet.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='maranet',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
