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
    version = "0.5",
    author = "Kiberpipa",
    author_email = "jakahudoklin@gmail.com",
    description = ("Pipa stream 3rd generation"),
    license = "GNU",
    keywords = "ffmpeg xmlrpc remote start",
    url = "https://github.com/offlinehacker/pipa_stream3",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    install_requires = [ "pystache", "pylirc2" ],
    entry_points="""
    [console_scripts]
    pstream3d= pipa_stream3.server_cli:main
    pstream3_client_lirc= pipa_stream3.client_lirc:main
    pstream3_client= pipa_stream3.client:main
    """,
    package_data={'pipa_stream3': ['templates/*.tpl']},
)
