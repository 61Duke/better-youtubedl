from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="betubedl",
    version="1.0.0",
    author="WEI HAITONG",
    author_email="loveweihaitong@foxmail.com",
    description="A Python library for downloading YouTube videos.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/WEIHAITONG1/better-youtube-downloader",
    packages=['betubedl'],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True,
)
