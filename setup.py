#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

setup(
    name="bv2mne",
    version='0.0.1',
    packages=find_packages(),
    author="David Meunier",
    description="Conversion from ",
    lisence='BSD 3',
    install_requires=['numpy',
                      'scipy',
                      'mne==0.18',
                      'nibabel',
                      'sklearn']
)
