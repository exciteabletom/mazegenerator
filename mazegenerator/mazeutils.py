# mazeutils - Tommy Dougiamas
import random

from . import g

maze = None


def get_cell_value(coords: tuple):
	"""
	Gets the value of the cell at the specified coordinates

	:param coords: tuple containing x and y values
	:return: value of the cell at the specifed coordinates
	"""
	try:
		return g.maze[coords[0]][coords[1]]
	# Sometimes we get an IndexError if the maze doesn't have borders
	# This solution is not perfect however, so it is still best practice to use borders
	except IndexError:
		return False


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


def get_cell_neighbours(coords: tuple, empty_cell=None):
	"""
	Gets the values of all cells that neighbour the cell at the specified coordinates

	:param coords: Tuple containing the x and y values of the cell to check the neighbours of
	:param empty_cell: specifies whether an empty cell is an 'int' or 'None'
	:return: coordinates of all neighbours that have not been visited in
				a list of tuples. Example: [(x,y), (x,y), (x,y)]
	"""
	# different tuples that contain the coords of all positions
	# relative to our input tuple
	left = (coords[0] - 1, coords[1])
	right = (coords[0] + 1, coords[1])
	up = (coords[0], coords[1] - 1)
	down = (coords[0], coords[1] + 1)

	# list containing all directional tuples
	all_dirs = [up, down, right, left]
	visitable_coordinates = []

	if type(empty_cell) == str:
		for dir in all_dirs:
			cell_value = get_cell_value(dir)

			if cell_value == empty_cell:
				if dir[0] == 0 or dir[0] == len(g.maze) - 1 \
					  or dir[1] == 0 or dir[1] == len(g.maze[0]) - 1:  # if edge piece
					continue

				if dir[0] < 0 or dir[1] < 0:  # If negative number
					continue

				visitable_coordinates.append(dir)  # Don't remove

	elif empty_cell == int:  # if we constructing a path from an enumerated maze
		for dir in all_dirs:
			cell_value = get_cell_value(dir)

			if type(cell_value) == int:  # if path has been visited
				visitable_coordinates.append(dir)

	return visitable_coordinates
