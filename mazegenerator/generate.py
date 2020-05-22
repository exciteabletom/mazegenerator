#!/usr/bin/env python3
"""
Creates a maze matrix that can be converted into an image:

The maze is compatible with mazesolver (https://github.com/exciteabletom/mazesolver)
The maze is represented in the matrix as follows:
 - Walls:   "#"
 - Paths:   "."
 - Start:   "s"
 - End:     "e"

There are two rules for the output matrix that make it compatible with mazesolver:

 - Walls around the entire maze
 - One entrance on the top row and one exit on the bottom row

Example output (5x5):

   [["#", "#", "#", "s", "#"],
    ["#", "#", ".", ".", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#"],
    ["#", "e", "#", "#", "#"]]
"""
from . import mazeutils as mu
from . import g

import os
import random
import sys  # for progress bar

random.seed(os.urandom(200))


def init_maze(width, height):
	"""
	Initialises a maze with only walls
	:param width: The width of the maze
	:param height: The height of the maze
	"""
	g.maze = []
	for x in range(width):
		g.maze.append([])
		for y in range(height):
			g.maze[-1].append("#")


def init_solution_path():
	"""
	Creates a randomized solution path through the maze.
	"""

	start_pos = random.randint(1, len(g.maze[0]) - 2)

	g.maze[0][start_pos] = "s"

	start = mu.get_cell_by_value("s")

	visited_cells = []  # Unordered list that stores all cells that have been already traversed.
	path_cells = []  # Stores cells that are in the final path.
	current_cell = (start[0] + 1, start[1])
	mu.set_cell_value(current_cell, ".")

	paths_done = False
	no_reverse = True
	last_progress_row = 0

	# Path from start
	while not paths_done:
		if (current_cell[0] % int(len(g.maze)/10) == 0 and current_cell[0] != last_progress_row)\
			  or current_cell[0] == len(g.maze) - 2:
			last_progress_row = current_cell[0]
			progress_percentage = int(current_cell[0] / (len(g.maze) - 2) * 100)
			sys.stdout.write(f"Generating maze: {progress_percentage}%\n")
			sys.stdout.flush()

		if current_cell[0] == len(g.maze) - 2:  # If on second last row of maze
			mu.set_cell_value((len(g.maze) - 1, current_cell[1]), "e")
			#mu.print_maze()
			break

		directions = mu.get_cell_neighbour_direction_names(current_cell, empty_cell="#")
		if no_reverse:
			try:
				directions.remove("up")
			except ValueError:  # If up is not in list
				pass

		rand_direction = directions[random.randint(0, len(directions) - 1)]

		# These lines favour right and left over up and down, so there is more horizontal movement in the path
		if "right" in directions and random.randint(0, 2) == 0:
			rand_direction = "right"
		elif "left" in directions and random.randint(0, 2) == 0:
			rand_direction = "left"

		if not rand_direction:
			breakpoint()

		if rand_direction == "up":
			no_reverse = True

		next_cell = mu.get_cell_neighbours(current_cell, "#", rand_direction)[0]

		mu.set_cell_value(next_cell, ".")

		if mu.next_to_edge(current_cell):
			no_reverse = True

		current_cell = next_cell


def expand_rows():
	"""
	'expands' rows by adding random paths on, above, and below the rows
	"""

	def branch(coords, direction):
		"""
		Branchs out to the side of a target cell, either left or right, used to add tree like structure
		:param coords: (x,y) indicating a cell position
		:param direction: 'left' or 'right'
		"""
		if direction == "left":
			opposite_direction = "right"
		else:
			opposite_direction = "left"

		while True:
			random_int = random.randint(0, 4)
			if random_int < 1:
				break

			neighbour_directions = mu.get_cell_neighbour_direction_names(coords, empty_cell="#")

			if direction in neighbour_directions:
				try:
					next_coords = mu.get_cell_neighbours(coords, "#", direction)[0]
				except IndexError:
					breakpoint()
				mu.set_cell_value(next_coords, ".")
				coords = next_coords
			else:
				# mu.print_maze()
				break

	for row_index, row in enumerate(g.maze):
		if row_index in (0, len(g.maze) - 1):
			continue

		for cell_index, cell in enumerate(row):
			if cell_index in (0, len(g.maze[0]) - 1):
				continue

			cell_coords = (row_index, cell_index)
			rand = random.randint(0, 10)

			if cell == "#":  # If cell is wall
				cell_neighbours = mu.get_cell_neighbours(cell_coords, empty_cell=".")

				if len(cell_neighbours) and rand < 4:
					mu.set_cell_value(cell_coords, ".")
				elif rand == 9:
					branch(cell_coords, "left")
				elif rand == 10:
					branch(cell_coords, "right")


def generate(width, height):
	"""
	Main function that creates the maze.
	:param width: Width of the matrix
	:param height: Height of the matrix
	"""
	init_maze(width, height)
	init_solution_path()

	expand_rows()
