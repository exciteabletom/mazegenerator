## __main__.py - Tommy Dougiamas
# This file interprets all command line arguments.
# It passes off the actual processing to other functions.

# Local imports
from . import generate  # width/height --> matrix
from . import create_output_image  # matrix --> image
from . import strings  # Static strings
from . import g  # global variables

# Stdlib imports
import sys
import os
from pathlib import Path  # Used to fix incompatibilities between windows and unix-based file paths "/" vs "\\"


def cmd_error(message=""):  # Display error message and exit the program with exit code 1
	if message:
		print(f"ERROR: {message}\n")

	print("See --help for more info.")
	exit(1)


def cmd_info(mode):  # Display information and exit the program with exit code 0
	if mode == "help":
		print(strings.help_message)

	elif mode == "version":
		print(strings.version)

	elif mode == "maze_rules":
		print(strings.maze_rules)

	else:
		raise ValueError(
			# If the mode was not valid warn, so then it doesn't get into prod
			f"DEV_ERROR: Option '{mode}' is not valid for cmd_info ")

	exit(0)


def main():
	output_dir = ""  # The directory for the picture to be outputted to
	width: int= 0
	height: int= 0

	cmd_args = sys.argv[1:]  # List storing all command line arguments passed to the program
	if len(cmd_args) == 0:  # if no arguments were given
		cmd_error("No arguments provided.")

	if "--help" in cmd_args or "-h" in cmd_args:
		cmd_info("help")

	elif "-v" in cmd_args or "--version" in cmd_args:
		cmd_info("version")

	skip_next_arg = False  # Boolean indicating whether the current iteration should be skipped

	# Loop handling arguments that have params like "-i" and "-o"
	for index, arg in enumerate(cmd_args):
		if skip_next_arg:
			skip_next_arg = False
			continue

		try:
			if arg == "-o" or arg == "--output":
				output_dir = cmd_args[index + 1]  # the argument after '-o' is the output path
				skip_next_arg = True  # We don't need to parse the next arg as it is a file-path

			elif arg == "-x" or arg == "--width":
				width = int(cmd_args[index + 1])
				skip_next_arg = True  # We don't need to parse the next arg as it is a file-path

			elif arg == "-y" or arg == "--height":
				height = int(cmd_args[index + 1])  # the argument after '-o' is the output path
				skip_next_arg = True  # We don't need to parse the next arg as it is a file-path

			elif arg == "-xy":
				height = int(cmd_args[index + 1])
				width = int(cmd_args[index + 1])
				skip_next_arg = True

			else:
				cmd_error(f"Option '{arg}' not recognised.")

		except IndexError:  # If no parameter is passed to the argument
			cmd_error(f"Option '{arg}' requires an parameter.")

	if not output_dir:
		output_dir = str(Path.cwd())
		print(f"No output directory supplied. Using default directory: '{output_dir}'")

	if not os.path.isdir(output_dir):
		cmd_error(f"Output directory '{output_dir}' doesn't exist or is not a directory")

	if not width or not height:
		cmd_error(f"Please supply a height and a width! Use -x and -y")

	if width < 20 or height < 20:
		cmd_error("Both width and height must be at least 20.")

	generate.generate(width, height)

	create_output_image.create(g.maze, output_dir)
