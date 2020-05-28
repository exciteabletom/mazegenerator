# Maze Generator

This program generates a random black and white maze image. The mazes that are generated can be solved with <a href="//github.com/exciteabletom/mazesolver">mazesolver</a>
   
## Installing

Check that your python version is >=3.5 with `python3 -V`.
Also make sure that pip is installed with `python3 -m pip -V`.

To install, simply run `python3 -m pip install mazegenerator --user` on the command line.

You can run the tool using `mazegenerator`(unix-based) or `mazegenerator.exe` (windows).

## How do I use it?

You can use `mazegenerator --help` to get a list of commands.

Normal usage will look something like this: `mazesolver -x 200 -y 300`


## What are the rules for maze images?
- Walls marked with black pixels and paths marked with white pixels

- Walls around the entire maze

- One entrance on the top row and one exit on the bottom row      
       
