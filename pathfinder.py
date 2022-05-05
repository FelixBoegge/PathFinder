import curses
from curses import wrapper
import queue
import time

maz = [["O", " ", " ", " ", "#"],
        [" ", "#", " ", "#", "#"],
        ["X", "#", "#", "#", "#"]
        ]


maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["O", " ", " ", " ", " ", "#", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#", "#", "#", " ", " ", " ", "#", "#", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ", " ", "#", "#", "#", " ", "#", "#", "#", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", " ", " ", "#", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#", "#", "#", "#", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", " ", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#", " ", "#", "#", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", "#", "#", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", "#", " ", "#", "#", " ", "#", "#", "#", " ", "#", "#", " ", " ", " ", " ", " ", "#"],
    ["#", "#", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", "#", "#", "#", "#", "#", " ", "#"],
    ["#", "#", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", "#", " ", "X"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
]

def print_maze(maze, stdscr, steps, path=[]):
    blue = curses.color_pair(1)
    red = curses.color_pair(2)
    green = curses.color_pair(3)
    stdscr.addstr(len(maze)+1, 1, "Steps: " + str(steps))
    stdscr.addstr(len(maze)+2, 1, "Path length: " + str(len(path)))
    for i, row in enumerate(maze):
        for j, v in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 3, "o", green)
            else:
                stdscr.addstr(i, j * 3, v, red)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, v in enumerate(row):
            if v == start:
                return i, j
    return None


def find_path_DFS(maze, stdscr):
    start = "O"
    end = "X"
    steps = 0
    start_pos = find_start(maze, start)

    s = []
    s.append((start_pos, [start_pos]))
    visited = set()

    while s:

        current_pos, path = s[-1]
        row, col = current_pos
        visited.add(current_pos)

        stdscr.clear()
        print_maze(maze, stdscr, steps, path)
        time.sleep(0.05)
        stdscr.refresh()
        steps += 1

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                s.append((neighbor, new_path))
        if s[-1][0] == current_pos:
            s.pop()
    return path


def find_path_BFS(maze, stdscr):
    start = "O"
    end = "X"
    steps = 0
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, steps, path)
        time.sleep(0.05)
        stdscr.refresh()
        steps += 1

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)


def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0 and maze[row-1][col] != "#":
        neighbors.append((row-1, col))                      # up
    if row + 1 < len(maze) and maze[row+1][col] != "#":
        neighbors.append((row+1, col))                      # down
    if col > 0 and maze[row][col-1] != "#":
        neighbors.append((row, col-1))                      # left
    if col + 1 < len(maze[0]) and maze[row][col+1] != "#":
        neighbors.append((row, col+1))                      # right
    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    #find_path_BFS(maze, stdscr)
    find_path_DFS(maze, stdscr)
    stdscr.getch()


wrapper(main)
