# -*- coding: utf-8
"""
Contains python package metadata, allowing mr_freeze to be installed with pip
"""
from setuptools import setup, find_packages

setup(
    name="mr_freeze",
    version="1.0",
    description="Reports measured variables from a cryostat",
    author="Michal Kononenko",
    author_email="mkononen@uwaterloo.ca",
    url='https://github.com/MichalKononenko/MrFreeze',
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "instrumentkit==0.3.1",
        "typing==3.5.3.0"
    ]
)
