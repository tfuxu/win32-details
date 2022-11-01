#!/usr/bin/env python3

import os

from setuptools import setup, find_packages
from setuptools.command.install import install as _install


with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()


setup(
    name="win32-details",
    license="GPL-3.0",
    version="0.5.0",
    author="tfuxu",
    description=".exe file details for your Nautilus file browser",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/tfuxu/win32-details",
    platforms=["Linux", "BSD"],
    keywords="nautilus extension exe details gnome",
    python_requires=">=3.6",

    project_urls={
        "Bug Tracker": "https://github.com/tfuxu/win32-details/issues",
        "Source Code": "https://github.com/tfuxu/win32-details"
    },

    classifiers=[
        "Development Status :: 4 - Beta",

        "Environment :: X11 Applications :: Gnome",

        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",

        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD",

        "Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",

        "Topic :: Utilities"
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyExifTool>=0.5.2"
    ],

    entry_points={
        "console_scripts": [
            "win32-details = win32_details.cli:cli_main"
        ]
    }
)
