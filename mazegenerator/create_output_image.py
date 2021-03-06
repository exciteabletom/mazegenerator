## create_final_image.py - Tommy Dougiamas
"""
Converts a matrix into a black and white image, and saves it to a specified directory
"""

from PIL import Image  # Pillow >=6.0
from pathlib import Path  # OS agnostic filesystem paths


def create(matrix: list, output_dir: str, output_name: str):
	"""
	Void function that marks the solution path into the image with green and saves the image.

	:param matrix: A matrix generated by generate.py (see generate.__doc__).
	:param output_dir: String with User-supplied path to a directory where the image will be saved.
	:param output_name: A name for the image file
	"""
	print("\nSaving Image... This may take a long time for bigger mazes")

	# open the image that was inputted
	output_image = Image.new("RGB", [len(matrix[0]), len(matrix)], (255, 255, 255))

	for y in range(0, len(matrix)):
		for x in range(0, len(matrix[-1])):
			cell = matrix[y][x]

			color = (0, 0, 0)  # By default color is black

			if cell == "." or cell == "s" or cell == "e":
				color = (255, 255, 255)  # Change color to black

			output_image.putpixel((x, y), color)

	out_path = Path(f"{output_dir}/{output_name}.jpg")  # Where the image will be saved to


	output_image.save(out_path, subsampling=0, quality=100)  # Save the image with no compression or sub-sampling

	print(f"Maze was saved at {out_path}")  # Make sure the user knows where the image was saved
