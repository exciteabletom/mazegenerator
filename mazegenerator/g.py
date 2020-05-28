maze = []


def change_string_length(string, length):
	"""
	Append spaces to a string until it reaches 'length'
	"""
	diff = length - len(string)
	return string + (" " * diff)
