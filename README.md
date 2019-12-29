Sudoku solver
=============

This is a python application made using [pyglet](https://pypi.org/project/pyglet/) for solving sudoku boards using the [backtracking algorithm](https://en.wikipedia.org/wiki/Backtracking).

Installation
============

First of all download the repository and place it anywhere on your machine. As I metioned before the application uses Python so it will need to be installed from [here](https://www.python.org/). It also requires that you have the [pyglet](https://pypi.org/project/pyglet/) package installed on your machine, you can do so with [pip](https://pypi.org/) using the command:
```bash
pip install pyglet
```
Or if you already downloaded the repository, then you can run this command while you are in the root directory.
```bash
pip install -r requirements.txt
```

Usage
============

The application can be launched with the following command:
```bash
python main.py
```
You can change the starting board by editing `board.txt` in the root directory. Each line must have 9 whitespace seperated values ranging from 0-9, 0 meaning that the cell is empty. There must be 9 lines for in total of 81 values. If the number of values wasn't 81 the board will be blank. Here is an example of how it should look like:
```
0 0 5 0 0 1 2 7 4
2 0 0 0 0 5 0 0 0
4 0 0 0 0 9 0 6 1
0 0 2 1 0 0 0 0 0
0 7 0 0 0 0 0 8 0
0 0 0 0 0 2 3 0 0
7 2 0 9 0 0 0 0 8
0 0 0 3 0 0 0 0 6
6 8 9 4 0 0 1 0 0
```

Screenshots
============

![Default board](https://i.imgur.com/2ZdysDk.png "Default board")  
![Check mistakes](https://i.imgur.com/0Dyb7oA.gif "Check mistakes")  
![Solve](https://i.imgur.com/np2Soky.gif "Solve")  
![Stepped solve](https://i.imgur.com/smZvhyn.gif "Stepped solve")

License
============
[MIT](LICENSE)
