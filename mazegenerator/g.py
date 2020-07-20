import os

# Maze Matrix
global maze
maze = []

# Seed used to seed the RNG
global seed 
seed = ""


def change_string_length(string, length):
	"""
	Append spaces to a string until it reaches 'length'
	"""
	diff = length - len(string)
	return string + (" " * diff)
