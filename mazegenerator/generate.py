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
    ["#", ".", ".", "#", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#"],
    ["#", "e", "#", "#", "#"]]
"""
from . import mazeutils as mu
from . import g

import os
import random

random.seed(os.urandom(200))


def init_maze(width, height):
	"""
	Initialises a maze with all walls except for an entrance and exit.
	"""
	g.maze = []
	for x in range(width):
		g.maze.append([])
		for y in range(height):
			g.maze[-1].append("#")

	start_pos = random.randint(1, 5)
	end_pos = random.randint(len(g.maze[-1]) - 5, len(g.maze[-1]) - 2)

	g.maze[0][start_pos] = "s"
	g.maze[1][start_pos] = 0

	g.maze[-1][end_pos] = "e"


def enumerate_maze():
	"""
	TODO
	"""
	counter = 0

	while True:  # Enumerate maze
		current_cells = mu.get_cells_by_value(counter)
		neighbours = []
		for cell in current_cells:
			for i in mu.get_cell_neighbours(cell, "#"):
				neighbours.append(i)

		if neighbours:
			for cell in neighbours:
				mu.set_cell_value(cell, counter + 1)
		else:
			break

		counter += 1

	start = mu.get_cell_by_value("s")

	mu.set_cell_value((start[0] + 1, start[1]), 0)


def init_solution_path():
	"""
	Creates a randomized solution path through the maze.
	"""
	end = mu.get_cell_by_value("e")
	counter = mu.get_cell_value((end[0] - 1, end[1]))  # To account for first cell being 0
	current_cell = (end[0] - 1, end[1])
	mu.set_cell_value(current_cell, ".")

	while True:
		raw_options = mu.get_cell_neighbours(current_cell, int)

		options = []
		for cell in raw_options:
			cell_value = mu.get_cell_value(cell)

			if cell_value == counter - 1:
				options.append(cell)

		random_cell_index = 0

		if len(options) > 1 and random.randint(0, 1) == 0:
			random_cell_index = random.randint(0, len(options) - 1)
		elif len(options) == 0:
			break

		random_cell = options[random_cell_index]
		mu.set_cell_value(random_cell, ".")

		current_cell = random_cell

		counter -= 1


def expand_row(row_index):
	"""
	'expands' rows by adding random paths on, above, and below the rows
	:param row_index: The row to expand.
	"""
	row = g.maze[row_index]
	for index, cell in enumerate(row):
		neighbours = mu.get_cell_neighbours((row_index, index), "#")
		for neighbour in neighbours:
			if random.randint(0, 10) <= 3:
				mu.set_cell_value(neighbour, ".")


def generate(width, height):
	"""
	Main function that creates the maze.
	:param width: Width of the matrix
	:param height: Height of the matrix
	:return: A maze matrix
	"""
	print("INITIALISING MAZE")
	init_maze(width, height)
	print("ENUMERATING MAZE")
	enumerate_maze()
	print("CREATING SOLUTION PATH")
	init_solution_path()
	print("PREPARING FOR ROW EXPANSION")
	for row_index, row in enumerate(g.maze):
		for cell_index, cell in enumerate(row):
			if type(cell) == int:
				g.maze[row_index][cell_index] = "#"

	for row in range(len(g.maze) - 1):
		if row % 2 == 0:
			print(f"EXPANDING ROW {row}")
			expand_row(row)

