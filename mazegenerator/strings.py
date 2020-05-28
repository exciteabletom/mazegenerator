## strings.py - Tommy Dougiamas
"""
This file contains all static strings.
"""

help_message = """\
Valid Commands
---------------
-h, --help    -  Prints this help page and exits.
-v, --version -  Prints the version of the program and exits.

-x, --width   -  The width of the maze. (required)
-y, --height  -  The height of the maze. (required)
--xy          -  The height and width of a square maze.

--no-noise    -  Render a solution path without any noise
--more-paths  -  Generate more paths
--more-walls  -  Generate more walls

-o, --output  -  Output filepath/directory

Example Usages 
---------------
mazegenerator -x 300 -y 2000 -o path/to/dir/my_cool_maze_name
mazegenerator --xy 600 --more-paths
mazegenerator --xy 200 -o path/to/dir/

Contact Info
---------------
Email: tom@digitalnook.net
Github: https://github.com/exciteabletom

Licensed under GPLv3: https://www.gnu.org/licenses/gpl-3.0.en.html \
"""

version = "1.0"
version_long = f"mazesolver{version}"

