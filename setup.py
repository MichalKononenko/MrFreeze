"""
Installs the application to the python directory
"""
from distutils.core import setup

setup(
    name="mr_freeze",
    version="1.0",
    description="Reports measured variables from a cryostat",
    author="Michal Kononenko",
    author_email="mkononen@uwaterloo.ca",
    packages=[
        "mr_freeze",
        "mr_freeze.devices",
        "mr_freeze.resources",
        "mr_freeze.tasks"
    ],
    install_requires=[
        "instrumentkit==0.3.1",
        "typing==3.5.3.0"
    ]
)
