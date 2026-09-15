import random
from collections import deque
import copy

def generate_random_coordinate(width, height):
    return (random.randint(0, height-1), random.randint(0, width-1))

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height 
        
        wall_count = int((width*height) * 0.50)
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        
        # Place walls randomly
        for _ in range(wall_count):
            x, y = generate_random_coordinate(width, height)
            while self.grid[x][y] == '#':
                x, y = generate_random_coordinate(width, height)
            self.grid[x][y] = '#'
        
        self.start_coor = generate_random_coordinate(width, height)
        self.goal_coor = generate_random_coordinate(width, height)
        while self.goal_coor == self.start_coor:
            self.goal_coor = generate_random_coordinate(width, height)
            
        self.grid[self.start_coor[0]][self.start_coor[1]] = 'S'
        self.grid[self.goal_coor[0]][self.goal_coor[1]] = 'G'
        
    def get_start(self):
        return self.start_coor
    
    def get_goal(self):
        return self.goal_coor
    
    def get_grid(self):
        return self.grid
    
    def get_neighbours(self, x, y):
        neighbours = []
        if x > 0 and self.grid[x-1][y] != '#':
            neighbours.append((x-1, y))
        if x < self.height - 1 and self.grid[x+1][y] != '#':
            neighbours.append((x+1, y))
        if y > 0 and self.grid[x][y-1] != '#':
            neighbours.append((x, y-1))
        if y < self.width - 1 and self.grid[x][y+1] != '#':
            neighbours.append((x, y+1))
        return neighbours
    
    def print_maze(self):
        for row in self.grid:
            print(' '.join(row))
            
def maze_bfs(maze):
    start = maze.get_start()
    goal = maze.get_goal()
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            maze_path = trace_back_path(came_from, current)
            return maze_path
        
        for neighbour in maze.get_neighbours(current[0], current[1]):
            if neighbour not in came_from:
                queue.append(neighbour)
                came_from[neighbour] = current
    
    return None


def trace_back_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]


def format_path(path):
    path_as_strings = [f"({x}, {y})" for x, y in path]
    return " ->".join(path_as_strings)

def star_maze_path(path, maze):
    maze_copy = copy.deepcopy(maze.grid[:][:])
    for x, y in path:
        if maze_copy[x][y] != 'G' and maze_copy[x][y] != 'S':
            maze_copy[x][y] = '*'
    return maze_copy

def maze_results(path, maze):
    if path:
        output_path = format_path(path)
        maze_copy = star_maze_path(path, maze)
        print("Path found:", output_path)
        for row in maze_copy:
            print(' '.join(row))
    else:
        print("No path found")
        
maze = Maze(10, 10)
maze_path = maze_bfs(maze)
maze_results(maze_path, maze)
