## __main__.py - Tommy Dougiamas
"""
This file interprets all command line arguments.
It passes off the actual processing to other functions.
"""

# Local imports
from . import generate  # width/height --> matrix
from . import create_output_image  # matrix --> image
from . import strings  # Static strings
from . import g  # global variables

# Stdlib imports
import sys
import os
from pathlib import Path  # Used to fix incompatibilities between windows and unix-based file paths ("/" vs "\\")


def cmd_error(message=""):  # Display error message and exit the program with exit code 1
	"""
	Displays a user-friendly error message and exits 1

	:param message: Message for error
	"""
	if message:
		print(f"ERROR: {message}\n")

	print("See --help for more info.")
	exit(1)


def cmd_info(mode):  # Display information and exit the program with exit code 0
	"""
	Displays a user friendly information string from 'strings' and exits 0.
	"""
	if mode == "help":
		print(strings.help_message)

	elif mode == "version":
		print(strings.version)

	elif mode == "maze_rules":
		print(strings.maze_rules)

	else:
		# If the mode was not valid throw error, so then it doesn't get into prod
		raise ValueError(
			f"DEV_ERROR: Option '{mode}' is not valid for cmd_info ")

	exit(0)


def main():
	"""
	Interprets command line arguments and passes on to generate.generate()
	Then runs create_output_image.create()

	Exit code 0 if successful, code 1 if error occurs
	"""
	output_path = ""  # The path for the picture to be outputted to
	width: int = 0
	height: int = 0

	option_no_noise = False
	option_more_paths = False
	option_more_walls = False

	cmd_args = sys.argv[1:]  # List storing all command line arguments passed to the program
	if len(cmd_args) == 0:  # if no arguments were given
		cmd_error("No arguments provided.")

	if "--help" in cmd_args or "-h" in cmd_args:
		cmd_info("help")

	elif "-v" in cmd_args or "--version" in cmd_args:
		cmd_info("version")

	elif "--maze-rules" in cmd_args:
		cmd_info("maze_rules")

	skip_next_arg = False  # Boolean indicating whether the current iteration should be skipped

	# Loop handling arguments that have params like "-i" and "-o"
	for index, arg in enumerate(cmd_args):
		if skip_next_arg:
			skip_next_arg = False
			continue

		try:
			if arg == "-o" or arg == "--output":
				output_path = cmd_args[index + 1]  # the argument after '-o' is the output path
				skip_next_arg = True

			elif arg == "-x" or arg == "--width":
				width = int(cmd_args[index + 1])
				skip_next_arg = True

			elif arg == "-y" or arg == "--height":
				height = int(cmd_args[index + 1])
				skip_next_arg = True

			elif arg == "-xy" or arg == "--xy":
				height = int(cmd_args[index + 1])
				width = int(cmd_args[index + 1])
				skip_next_arg = True

			elif arg == "--no-noise":
				option_no_noise = True

			elif arg == "--more-walls":
				option_more_walls = True

			elif arg == "--more-paths":
				option_more_paths = True

			else:
				cmd_error(f"Option '{arg}' not recognised.")

		except IndexError:  # If no parameter is passed when an arg expects it
			cmd_error(f"Option '{arg}' requires an parameter.")

	# This block is designed to work if:
	# 1. Only a directory name is passed with or without a trailing '/' eg Pictures/ and Pictures
	# 2. An image name is passed with/without a .jpg extension  eg. mymaze.jpg and mymaze
	# 3. A directory name is passed with an image name  eg. Pictures/mymaze.jpg or Pictures/mymaze
	output_dir = str(Path.cwd())
	output_name = "maze"
	if output_path:
		if os.path.isdir(output_path):  # If only directory is specified
			output_dir = output_path
		else:
			path_lst = output_path.split("/")
			if path_lst[-1] == "":  # If directory was specified, but not valid
				cmd_error("Invalid directory name.")

			elif len(path_lst) == 1:  # If only image name is specified with no directory
				output_name = path_lst[0].replace(".jpg", "").replace(".jpeg", "")

			else:  # If directory and image name are specified
				output_name = path_lst[-1]
				output_dir = output_path[0:-len(output_name)]
				output_name = output_name.replace(".jpg", "").replace(".jpeg", "")

	if not width or not height:
		cmd_error(f"Please supply a height and a width! Use -x and -y")

	if width < 20 or height < 20:  # Generation doesn't work with super small mazes
		cmd_error("Both width and height must be at least 20.")

	noise_bias = "default"

	if option_no_noise:  # creates only a path
		noise_bias = "none"
	elif option_more_paths:
		noise_bias = "paths"
	elif option_more_walls:
		noise_bias = "walls"

	generate.generate(width, height, noise_bias)

	create_output_image.create(g.maze, output_dir, output_name)
