## generate.py - Created by Tommy Dougiamas as a part of mazegenerator
"""
This file contains all functions that create a random maze matrix.
The maze is compatible with mazesolver (https://github.com/exciteabletom/mazesolver)
The maze is represented in the matrix as follows:
 - Walls:   "#"
 - Paths:   "."
 - Start:   "s"
 - End:     "e"

There are two rules for the output matrix that make it compatible with mazesolver:

 - Walls around the entire maze
 - One entrance on the top row and one exit on the bottom row

 Example maze matrix output:
	TODO
"""
from . import g
import random
import os

random.seed(os.urandom(200))  # Seed the random generator with random bytes


def get_cells_by_value(value):
	"""
	Get cell coordinates based on the value of the cell.

	:param value: The value to search cells for
	:return: list of all coordinates that contain the specified value
	"""
	all_matching_cells = []  # the list containing all the coordinates of cells
	for row_index, row in enumerate(g.maze):
		for column_index, cell in enumerate(row):
			if cell == value:
				all_matching_cells.append((row_index, column_index))

	return all_matching_cells


def get_cell_by_value(value):
	"""
	The same as get_cells_by_value, except raises a ValueError if there is more than one cell with that value

	:param value: The value to search cells for
	:raises ValueError: If more then one of the value is found in the maze.
	:return: the cell coordinate that contains the value
	"""
	values = get_cells_by_value(value)
	if len(values) > 1:
		raise ValueError(f"Expected only one cell to have value '{value}'. {len(values)} cells contained the value.")

	return values[0]


def set_cell_value(coords: tuple, value: str or int):
	"""
	Sets the value of a cell at the specified coordinates.

	:param coords: The coordinates of the cell to be changed
	:param value: The value we want the cell to be set to
	"""
	g.maze[coords[0]][coords[1]] = value


def check_cell_exists(coords):
	"""
	Checks if a cell exists within the maze
	:param coords: A tuple (x,y), representing a cell
	:return bool: True if cell exists, False otherwise
	"""
	try:
		_ = g.maze[coords[0]][coords[1]]  # Will throw IndexError if the cell is out of the maze area
		return True  # Cell exists
	except IndexError:
		return False  # Cell doesn't exist


def get_random_neighbour(coords):
	"""
	Gets a random cell neighbouring the cell at coords
	:param coords: Tuple (x,y), containing coordinates to a cell in g.maze
	:return: Coordinates of a cell neighbouring the one at coords, selected at random
	"""
	# different tuples that contain the coords of all positions
	# relative to our input tuple
	left = (coords[0] - 1, coords[1])
	right = (coords[0] + 1, coords[1])
	up = (coords[0], coords[1] - 1)
	down = (coords[0], coords[1] + 1)

	# list containing all directional tuples
	all_dirs = [left, right, up, down]
	neighbours = []

	for dir in all_dirs:
		try:
			_ = g.maze[dir[0]][dir[1]]
			neighbours.append(dir)

		except IndexError:
			pass

	if len(neighbours) == 0:
		raise ValueError("Could not find any neighbouring cells.")

	rand_neighbour = neighbours[random.randint(0, len(neighbours) - 1)]
	return rand_neighbour


def generate():
	make_random_inital_path()
