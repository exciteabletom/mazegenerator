#!/usr/bin/env python3
from setuptools import setup
import sys
from mazegenerator import strings

print(strings.version)
with open("./README.md", encoding="utf-8") as readme:
	long_description = readme.read()

setup(
	name="mazegenerator",
	version=strings.version,

	description="A maze generation algorithm for image-based mazes.",
	long_description=long_description,
	long_description_content_type="text/markdown",

	url="https://github.com/exciteabletom/mazegenerator",
	author="Tommy Dougiamas",
	author_email="tom@digitalnook.net",

	classifiers=[
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3"
	],

	entry_points={
		"console_scripts": ["mazegenerator = mazegenerator.__main__:main"],
	},

	keywords="maze algorithm image generate",

	packages=["mazegenerator"],

	python_requires=">=3.5",

	install_requires=["Pillow>=6.0"]
)
