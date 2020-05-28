## mazeutils.py - Tommy Dougiamas
"""
Some basic utilites for manipulating and displaying the variable g.maze.
"""
import random
from . import g

maze = None


def print_maze():
	"""
	Prints out the maze matrix in a human readable format, useful for debugging.
	"""
	for i in g.maze:
		print(i)
	print("\n")


def get_cell_value(coords: tuple):
	"""
	Gets the value of the cell at the specified coordinates

	:param coords: tuple containing x and y values
	:return: value of the cell at the specifed coordinates
	"""
	try:
		return g.maze[coords[0]][coords[1]]
	# Sometimes we get an IndexError if the maze doesn't have borders
	# This solution is not perfect, so it is still best practice to use borders
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


def is_edge(coords):
	"""
	Check if a piece is an edge or not.

	:param coords: A tuple (x,y)
	:return: True if piece is an edge piece False otherwise
	"""
	if coords[0] == 0 or coords[0] == len(g.maze) - 1 \
		  or coords[1] == 0 or coords[1] == len(g.maze[0]) - 1:  # if edge piece
		return True

	return False


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


def set_cell_value(coords: tuple, value: any):
	"""
	Sets the value of a cell at the specified coordinates.

	:param coords: The coordinates of the cell to be changed
	:param value: The value we want the cell to be set to
	"""
	g.maze[coords[0]][coords[1]] = value


def check_cell_exists(coords):
	"""
	Checks if a cell exists within the maze.

	:param coords: A tuple (x,y), representing a cell
	:return bool: True if cell exists, False otherwise
	"""
	try:
		_ = g.maze[coords[0]][coords[1]]  # Will throw IndexError if the cell is out of the maze area
		return True  # Cell exists
	except IndexError:
		return False  # Cell doesn't exist


def get_cell_neighbours(coords: tuple, empty_cell=None, directions=None):
	"""
	Gets the values of all cells that neighbour the cell at the specified coordinates

	:param coords: Tuple containing the x and y values of the cell to check the neighbours of
	:param empty_cell: specifies whether an empty cell is an int or a specific string
	:param directions: String containing directions to be checked for.
	:return: coordinates of all neighbours that have not been visited in
				a list of tuples. Example: [(x,y), (x,y), (x,y)]
	"""
	# different tuples that contain the coords of all positions
	# relative to our input tuple
	up = (coords[0] - 1, coords[1])
	down = (coords[0] + 1, coords[1])
	left = (coords[0], coords[1] - 1)
	right = (coords[0], coords[1] + 1)

	# list containing all directional tuples
	all_dirs = [up, down, right, left]
	if directions:
		all_dirs = []
		if "up" in directions:
			all_dirs.append(up)
		if "down" in directions:
			all_dirs.append(down)
		if "right" in directions:
			all_dirs.append(right)
		if "left" in directions:
			all_dirs.append(left)

		if not all_dirs:
			raise ValueError(f"Directions {directions} not recognised.")

	visitable_coordinates = []

	if type(empty_cell) == str:
		for dir in all_dirs:
			cell_value = get_cell_value(dir)

			if cell_value == empty_cell:
				if is_edge(dir):
					continue

				if dir[0] < 0 or dir[1] < 0:  # If negative number
					continue

				visitable_coordinates.append(dir)  # Don't remove

	elif empty_cell == int:  # interpret any int as an empty cell
		for dir in all_dirs:
			cell_value = get_cell_value(dir)

			if type(cell_value) == int:  # if path has been visited
				visitable_coordinates.append(dir)

	return visitable_coordinates


def get_cell_neighbour_direction_names(coords, direction="all", empty_cell="."):
	"""
	Checks which directions can be moved to.

	:param coords: A tuple (x,y).
	:param direction: String containing a directions to check. If left out will check every directions.
	:param empty_cell: What value is considered empty
	:return: A list containing directions that can be moved to. E.g. ["right", "up", "left"].
	"""

	# different tuples that contain the coords of all positions
	# relative to our input tuple
	up = (coords[0] - 1, coords[1])
	down = (coords[0] + 1, coords[1])
	left = (coords[0], coords[1] - 1)
	right = (coords[0], coords[1] + 1)

	all_dirs = [(up, "up"), (down, "down"), (right, "right"), (left, "left")]
	good_dirs = []

	# The following is messy and slow TODO
	if direction == "all":
		for cell_data in all_dirs:
			if is_edge(cell_data[0]) or get_cell_value(cell_data[0]) != empty_cell:
				continue
			good_dirs.append(cell_data[1])

	else:
		if direction == "up":
			index = 0
		elif direction == "down":
			index = 1
		elif direction == "right":
			index = 2
		elif direction == "left":
			index = 3
		else:
			raise ValueError(f"Direction {direction}, not recognised.")

		if get_cell_value(all_dirs[index]) == empty_cell and not is_edge(all_dirs[index]):
			good_dirs.append(direction)

	return good_dirs


def next_to_edge(coords: tuple):
	"""
	Function for checking if a cell is next to the edge of the maze.

	:param coords: Tuple (x, y)
	:rtype: bool
	:return: True if next to edge, false otherwise
	"""
	next_to_wall: bool = False

	if coords[0] == 1 or coords[0] == len(g.maze) - 2:
		next_to_wall = True

	elif coords[1] == 1 or coords[1] == len(g.maze[-1]) - 2:
		next_to_wall = True

	return next_to_wall
