## strings.py - Tommy Dougiamas
"""
This file contains all constant strings.
"""

HELP = """\
Valid Commands
---------------
-h, --help      -  Prints this help page and exits.
-v, --version   -  Prints the version of the program and exits.
--maze-rules    -  Prints the rules for maze images.

-x, --width     -  The width of the maze. (required)
-y, --height    -  The height of the maze. (required)
--xy            -  The height and width of a square maze.

--no-noise      -  Render a solution path without any noise
--favour-paths  -  Generate more paths
--favour-walls  -  Generate more walls

-s, --seed      -  Specifies a seed to be used for the random number generator
-o, --output    -  Output filepath/directory

Example Usages 
---------------
mazegenerator -x 300 -y 2000 -o path/to/dir/my_cool_maze_name
mazegenerator --xy 600 --favour-paths
mazegenerator --xy 200 -o path/to/dir/

Contact Info
---------------
Email: tom@digitalnook.net
Github: https://github.com/exciteabletom

Licensed under GPLv3: https://www.gnu.org/licenses/gpl-3.0.en.html \
"""

MAZE_RULES = """\
What are the rules for maze images?
---------------

- Walls marked with black pixels and paths marked with white pixels

- Walls around the entire maze

- One entrance on the top row and one exit on the bottom row
 
Check out some of the example mazes at https://github.com/exciteabletom/mazegenerator/tree/master/examples \
"""


VERSION = "1.2.1"
VERSION_LONG = f"mazegenerator{VERSION}"

