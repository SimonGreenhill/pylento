#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = 0.1
DESCR = "A python tool for calculating split support and generating Lento plots"

setup(
    name='PyLento',
    version=VERSION,
    description=DESCR,
    long_description="",
    url='https://github.com/SimonGreenhill/pylento',
    author='Simon J. Greenhill',
    author_email='simon@simon.net.nz',
    license='BSD',
    zip_safe=True,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='phylogenetics lento',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=2.0.2',
        'python-nexus>=1.4.2',
        'python-newick>=0.7.0',
    ],
    entry_points={
        'console_scripts': [
            'pylento = pylento.cli:main'
        ],
    },
    test_suite="pylento.test_pylento",
)
