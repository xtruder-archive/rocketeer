import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a 
# top level
# README file and 2) it's easier to type in the README file than to put 
# a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pipa_stream3",
    version = "0.1",
    author = "Jaka Hudoklin",
    author_email = "jakahudoklin@gmail.com",
    description = ("Start ffmpeg processes remotely and view status."),
    license = "BSD",
    keywords = "ffmpeg xmlrpc remote start",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=find_packages(),
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires = [ "pystache" ],
    entry_points="""
    [console_scripts]
    pipa_stream3= pipa_stream3.cli:main
    """,
)
