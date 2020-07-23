"""
Creates a randomised maze matrix that can be converted into an image.
It is assumed that the global maze matrix is stored at ./g.py:maze.

The maze is compatible with mazesolver (https://github.com/exciteabletom/mazesolver)

There are two rules for the output matrix that make it compatible:

 - Walls around the entire maze
 - One entrance on the top row and one exit on the bottom row

The maze is represented in the matrix as follows:
 - Walls:   "#"
 - Paths:   "."
 - Start:   "s"
 - End:     "e"

Example output (5x5):

   [["#", "#", "#", "s", "#"],
    ["#", "#", ".", ".", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", "e", "#", "#", "#"]]
"""
## generate.py - Tommy Dougiamas

# Standard libraries
import os
import random

# Third party
import progress.bar  # Progress bars

# Relative
from . import mazeutils as mu
from . import g


def check_seed():
	"""
	Creates a random seed if one is not defined already
	"""
	if not g.seed:  # If no user-defined seed
		# Create random seed
		random_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                            "t", "u", "v", "w" "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
		for _ in range(15):
			rand_bool = random.random() < 0.5
			rand_char = random_chars[random.randint(0, len(random_chars) - 1)]

			if rand_bool:
				rand_char = rand_char.upper()

			g.seed = g.seed + rand_char

	print(f"Using seed '{g.seed}'\n")
	random.seed(g.seed)


def init_maze(width, height):
	"""
	Initialises a maze with only walls
	:param width: The width of the maze
	:param height: The height of the maze
	"""
	g.maze = []

	progress_bar = progress.bar.PixelBar(g.change_string_length("Initialising empty maze", 30), max=height)

	for _ in range(height):
		progress_bar.next()
		g.maze.append([])
		for _ in range(width):
			g.maze[-1].append("#")

	progress_bar.finish()


def branch(coords: tuple, direction: str, no_exit: bool = False, noise_offset: float = 0.0):
	"""
	Branches out to the side of a target cell, either left, right or down, used to add tree like structure

	:param coords: (x,y) indicating a cell position
	:param direction: 'left', 'right' or 'down'
	:param no_exit: Bool indicating whether to not stop randomly
	:param noise_offset: float that affects some of the random chances
	:return: The cell that was last visited
	:rtype: tuple
	"""

	while True:
		rand_float = random.random() + noise_offset
		if rand_float < 0.05 and not no_exit:
			return coords

		neighbour_directions = mu.get_cell_neighbour_direction_names(coords, empty_cell="#")

		if direction in neighbour_directions:
			final_direction = direction
			if 0.05 < rand_float < 0.45 + noise_offset:
				final_direction = "down"

			try:
				next_coords = mu.get_cell_neighbours(coords, "#", final_direction)[0]
			except IndexError:
				return coords

			if not mu.is_edge(next_coords):
				if next_coords[0] == len(g.maze) - 1:
					breakpoint()
				mu.set_cell_value(next_coords, ".")
				coords = next_coords
			else:
				return coords
		else:
			return coords


def init_solution_path():
	"""
	Creates a randomized solution path through the maze.
	"""

	# Find the beginning of the maze
	start_pos = random.randint(1, len(g.maze[0]) - 2)
	g.maze[0][start_pos] = "s"
	start = mu.get_cell_by_value("s")

	# Set the current cell to be the cell under start
	current_cell = (start[0] + 1, start[1])
	mu.set_cell_value(current_cell, ".")

	# TODO: Implement the possibility of the path going up
	# Currently no_up will always be True meaning the path can never go upwards
	no_up = True

	if random.random() < 0.5:
		h_prefer = "right"
		not_h_prefer = "left"
	else:
		h_prefer = "left"
		not_h_prefer = "right"

	rows = len(g.maze) - 2
	last_row = 0

	progress_bar = progress.bar.PixelBar(g.change_string_length("Generating random solution", 30), max=rows)

	# Path from start
	while True:
		if current_cell[0] != last_row:
			last_row = current_cell[0]
			progress_bar.next()

		if current_cell[0] == len(g.maze) - 2:  # If on second last row of maze
			mu.set_cell_value((len(g.maze) - 1, current_cell[1]), "e")
			break

		# Possible directions we could travel to
		directions = mu.get_cell_neighbour_direction_names(current_cell, empty_cell="#")

		if no_up and "up" in directions:  # Currently will always be triggered
			directions.remove("up")

		# A random direction
		rand_direction = directions[random.randint(0, len(directions) - 1)]

		if h_prefer in directions and random.random() < 0.6:
			rand_direction = h_prefer

		elif random.random() < 0.01:
			current_cell = branch(current_cell, h_prefer)
			progress_bar.next(current_cell[0] - last_row)
			last_row = current_cell[0]
			if random.random() < 0.5:
				h_prefer, not_h_prefer = (not_h_prefer, h_prefer)
			continue

		next_cell = mu.get_cell_neighbours(current_cell, "#", rand_direction)[0]
		mu.set_cell_value(next_cell, ".")

		if mu.next_to_edge(current_cell):
			if random.random() < 0.60:
				h_prefer, not_h_prefer = (not_h_prefer, h_prefer)

		current_cell = next_cell

	progress_bar.finish()


def expand_rows(noise_offset: float):
	"""
	'expands' rows by adding random paths on, above, and below the rows
	:param noise_offset: An offset applied to some of the random float values generated
	                        A negative offset reduces noise, a positive one increases noise
	"""
	progress_bar = progress.bar.PixelBar(g.change_string_length("Adding noise", 30), max=len(g.maze))

	for row_index, row in enumerate(g.maze):
		progress_bar.next()
		if row_index % 3 == 0:
			continue

		if row_index == len(g.maze) - 1:
			continue

		for cell_index, cell in enumerate(row):
			if cell_index in (0, len(g.maze[0]) - 1):
				continue

			cell_coords = (row_index, cell_index)
			rand = random.randint(0, 13)

			if cell == "#":  # If cell is wall
				cell_neighbours = mu.get_cell_neighbours(cell_coords, empty_cell=".")

				if cell_neighbours and rand < 1:
					mu.set_cell_value(cell_coords, ".")
				elif rand in (2, 3):
					rand_direction = ""

					# Rare wildcard for more randomness TODO: Maybe too expensive to compute? 
					if random.random() < 0.005:
						rand_direction = "down"
					elif rand == 2:
						rand_direction = "left"
					elif rand == 3:
						rand_direction = "right"
					else:
						raise ValueError("DEVERROR: Random integer out of range")

					branch(cell_coords, rand_direction, random.random() < 0.001, noise_offset)

	progress_bar.finish()


def generate(width: int, height: int, noise_bias: str):
	"""
	Main function that creates the maze.
	:param width: Width of the matrix
	:param height: Height of the matrix
	:param noise_bias: Either "wall", "less", "none", or and empty string indicating no bias
	"""
	check_seed()
	init_maze(width, height)
	init_solution_path()

	if noise_bias != "none":  # If we should generate noise
		noise_offset = 0

		if noise_bias == "walls":  # Draw less paths
			print("Creating more walls")
			noise_offset = -0.09

		elif noise_bias == "paths":  # Draw more paths
			print("Creating more paths")
			noise_offset = 0.25

		expand_rows(noise_offset)
	else:
		print("Only rendering solution path")
