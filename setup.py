import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "usbdio32",
    version = "0.7.9",
    author = "ALexander Depillis",
    description = "An easy-to-use python class-based interface to the Acces USB DIO-32 Digital Interface module",
    long_description=read('README.md'),
    packages=['usbdio',],
)
