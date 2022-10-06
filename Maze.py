from enum import Enum


import enum

class Wall(Enum):
    SOUTH = 1
    WEST = 2

class Cell:
    def __init__(self):
        self.cordinates = [0,0]
        self.wall_south = False
        self.wall_west = False
        self.visited = False

    def reset_cell(self):
        self.wall_south = False
        self.wall_west = False
        self.visited = False

class Maze:
    def __init__(self, size):
        self.size = size
        #self.maze = [[Cell() for _ in range(size)] for _ in range(size)]

        maze = []
        for row in range(size):
            row_list = []
            for col in range(size):
                cell = Cell()
                cell.cordinates = [row, col]
                row_list.append(cell)
            maze.append(row_list)

        self.maze = maze

        self.cell_width = 2
        self.wall_thickness = 0.1
        self.wall_height = 2

    def set_cell(self, cell, wall):
        if wall == Wall.SOUTH:
            self.maze[cell.cordinates[0]][cell.cordinates[1]].wall_south = True
        elif wall == Wall.WEST:
            self.maze[cell.cordinates[0]][cell.cordinates[1]].wall_west = True

    def reset_maze(self):
        for row in self.maze:
            for cell in row:
                cell.reset_cell()

    def set_small_3_maze(self):
        self.set_cell(self.maze[0][0], Wall.SOUTH)
        self.set_cell(self.maze[0][1], Wall.SOUTH)
        self.set_cell(self.maze[1][2], Wall.WEST)
        self.set_cell(self.maze[2][1], Wall.WEST)

    def set_random_maze(self):
        start_point = [0,0]
        end_point = [self.size - 1, self.size - 1]
        curr_point = start_point
        run_alg = True
        visited_cells = []

        for row in self.maze:
            for cell in row:
                self.set_cell(cell, Wall.SOUTH)
                self.set_cell(cell, Wall.WEST)

        visit_cell = self.maze[curr_point[0], curr_point[1]]
        visit_cell.visited = True
        visited_cells.append[visit_cell]

        while run_alg:
            # TODO: choose random location relative to current location, ...
            pass


    def to_string(self):
        res = "__" * len(self.maze) + "__\n"

        for row in self.maze:
            res += "|"
            for cell in row:
                if cell.wall_south & cell.wall_west:
                    res += "|_"
                elif cell.wall_south:
                    res += " _"
                elif cell.wall_west:
                    res += "| "
                else:
                    res += "  "
            res += "|\n"
        res += "__" * len(self.maze) + "__"
        return res
