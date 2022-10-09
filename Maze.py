from enum import Enum


import enum
import random

class Wall(Enum):
    SOUTH = 1
    WEST = 2

class Object(Enum):
    PYRAMID = 1

class CellCord:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Cell:
    def __init__(self, row, col):
        self.cord = CellCord(row, col)
        self.wall_south = False
        self.wall_west = False
        self.visited = False
        self.object = None

    def reset_cell(self):
        self.wall_south = False
        self.wall_west = False
        self.visited = False

    def to_string(self):
        return "[" + str(self.cord.row) + "][" + str(self.cord.col) + "]"

class Maze:
    def __init__(self, size):
        self.size = size

        maze = []
        for row in range(size):
            row_list = []
            for col in range(size):
                cell = Cell(row, col)
                row_list.append(cell)
            maze.append(row_list)

        self.maze = maze

        self.cell_width = 4
        self.wall_thickness = 0.2
        self.wall_height = 2

        self.prev_cell = self.maze[1][0]
        self.curr_cell = self.maze[0][0]

    def set_cell(self, cell, wall):
        if wall == Wall.SOUTH:
            self.maze[cell.cord.row][cell.cord.col].wall_south = True
        elif wall == Wall.WEST:
            self.maze[cell.cord.row][cell.cord.col].wall_west = True

    def reset_maze(self):
        for row in self.maze:
            for cell in row:
                cell.reset_cell()

    def set_small_3_maze(self):
        self.set_cell(self.maze[0][0], Wall.SOUTH)
        self.set_cell(self.maze[0][1], Wall.SOUTH)
        self.set_cell(self.maze[1][0], Wall.SOUTH)
        self.set_cell(self.maze[1][2], Wall.WEST)
        self.set_cell(self.maze[2][1], Wall.WEST)
        self.set_cell(self.maze[2][2], Wall.WEST)

    def set_10_maze(self):
        #row 1
        self.set_cell(self.maze[0][1], Wall.SOUTH)
        self.set_cell(self.maze[0][2], Wall.SOUTH)
        self.set_cell(self.maze[0][3], Wall.SOUTH)
        self.set_cell(self.maze[0][4], Wall.SOUTH)
        self.set_cell(self.maze[0][5], Wall.SOUTH)
        self.set_cell(self.maze[0][6], Wall.SOUTH)
        self.set_cell(self.maze[0][7], Wall.SOUTH)
        self.set_cell(self.maze[0][8], Wall.SOUTH)
        self.set_cell(self.maze[0][9], Wall.SOUTH)
        #row 2
        self.set_cell(self.maze[1][1], Wall.WEST)
        self.set_cell(self.maze[1][2], Wall.SOUTH)
        self.set_cell(self.maze[1][5], Wall.WEST)
        self.set_cell(self.maze[1][7], Wall.SOUTH)
        self.set_cell(self.maze[1][8], Wall.SOUTH)
        self.set_cell(self.maze[1][9], Wall.SOUTH)
        self.set_cell(self.maze[1][10], Wall.WEST)
        #row 3
        self.set_cell(self.maze[2][1], Wall.SOUTH)
        self.set_cell(self.maze[2][2], Wall.SOUTH)
        self.set_cell(self.maze[2][3], Wall.WEST)
        self.set_cell(self.maze[2][4], Wall.SOUTH)
        self.set_cell(self.maze[2][4], Wall.WEST)
        self.set_cell(self.maze[2][5], Wall.WEST)
        self.set_cell(self.maze[2][6], Wall.WEST)
        self.set_cell(self.maze[2][6], Wall.SOUTH)
        self.set_cell(self.maze[2][10], Wall.WEST)
        #row 4
        self.set_cell(self.maze[3][1], Wall.WEST)
        self.set_cell(self.maze[3][4], Wall.SOUTH)
        self.set_cell(self.maze[3][6], Wall.WEST)
        self.set_cell(self.maze[3][7], Wall.SOUTH)
        self.set_cell(self.maze[3][9], Wall.SOUTH)
        self.set_cell(self.maze[3][10], Wall.WEST)
        #row 5
        self.set_cell(self.maze[4][1], Wall.WEST)
        self.set_cell(self.maze[4][2], Wall.WEST)
        self.set_cell(self.maze[4][3], Wall.WEST)
        self.set_cell(self.maze[4][3], Wall.SOUTH)
        self.set_cell(self.maze[4][5], Wall.WEST)
        self.set_cell(self.maze[4][6], Wall.WEST)
        self.set_cell(self.maze[4][6], Wall.SOUTH)
        self.set_cell(self.maze[4][8], Wall.WEST)
        self.set_cell(self.maze[4][9], Wall.WEST)
        self.set_cell(self.maze[4][10], Wall.WEST)
        #row 6
        self.set_cell(self.maze[5][1], Wall.WEST)
        self.set_cell(self.maze[5][2], Wall.WEST)
        self.set_cell(self.maze[5][2], Wall.SOUTH)
        self.set_cell(self.maze[5][4], Wall.WEST)
        self.set_cell(self.maze[5][4], Wall.SOUTH)
        self.set_cell(self.maze[5][5], Wall.WEST)
        self.set_cell(self.maze[5][6], Wall.WEST)
        self.set_cell(self.maze[5][7], Wall.WEST)
        self.set_cell(self.maze[5][8], Wall.WEST)
        self.set_cell(self.maze[5][9], Wall.WEST)
        self.set_cell(self.maze[5][10], Wall.WEST)
        #row 7
        self.set_cell(self.maze[6][1], Wall.WEST)
        self.set_cell(self.maze[6][1], Wall.SOUTH)
        self.set_cell(self.maze[6][3], Wall.SOUTH)
        self.set_cell(self.maze[6][3], Wall.WEST)
        self.set_cell(self.maze[6][5], Wall.SOUTH)
        self.set_cell(self.maze[6][6], Wall.SOUTH)
        self.set_cell(self.maze[6][6], Wall.WEST)
        self.set_cell(self.maze[6][8], Wall.SOUTH)
        self.set_cell(self.maze[6][8], Wall.WEST)
        #row 8
        self.set_cell(self.maze[7][1], Wall.WEST)
        self.set_cell(self.maze[7][2], Wall.SOUTH)
        self.set_cell(self.maze[7][3], Wall.WEST)
        self.set_cell(self.maze[7][4], Wall.SOUTH)
        self.set_cell(self.maze[7][5], Wall.SOUTH)
        self.set_cell(self.maze[7][6], Wall.WEST)
        self.set_cell(self.maze[7][7], Wall.SOUTH)
        self.set_cell(self.maze[7][8], Wall.SOUTH)
        self.set_cell(self.maze[7][10], Wall.WEST)
        #row 9
        self.set_cell(self.maze[8][1], Wall.WEST)
        self.set_cell(self.maze[8][3], Wall.SOUTH)
        self.set_cell(self.maze[8][4], Wall.WEST)
        self.set_cell(self.maze[8][5], Wall.WEST)
        self.set_cell(self.maze[8][6], Wall.SOUTH)
        self.set_cell(self.maze[8][7], Wall.WEST)
        self.set_cell(self.maze[8][8], Wall.WEST)
        self.set_cell(self.maze[8][8], Wall.SOUTH)
        self.set_cell(self.maze[8][10], Wall.WEST)
        #row 10
        self.set_cell(self.maze[9][1], Wall.SOUTH)
        self.set_cell(self.maze[9][1], Wall.WEST)
        self.set_cell(self.maze[9][2], Wall.SOUTH)
        self.set_cell(self.maze[9][3], Wall.SOUTH)
        self.set_cell(self.maze[9][3], Wall.WEST)
        self.set_cell(self.maze[9][4], Wall.SOUTH)
        self.set_cell(self.maze[9][5], Wall.SOUTH)
        self.set_cell(self.maze[9][6], Wall.SOUTH)
        self.set_cell(self.maze[9][7], Wall.SOUTH)
        self.set_cell(self.maze[9][7], Wall.WEST)
        self.set_cell(self.maze[9][8], Wall.SOUTH)
        self.set_cell(self.maze[9][9], Wall.SOUTH)
        self.set_cell(self.maze[9][10], Wall.WEST)

    def set_random_maze(self):
        start_cell = self.maze[self.size - 1][self.size - 1]
        end_cell = self.maze[0][0]
        curr_cell = start_cell
        run_alg = True
        visited_cells = []

        for row in self.maze:
            for cell in row:
                self.set_cell(cell, Wall.SOUTH)
                self.set_cell(cell, Wall.WEST)

        visit_cell = self.maze[curr_cell.row][curr_cell.col]
        visit_cell.visited = True
        visited_cells.append(visit_cell)

        while run_alg:
            # TODO: choose random location relative to current location, ...
            dir = random.randint(1,4)
            print(dir)

            if dir == 1:
                # up
                visit_cell = self.maze[curr_cell.row - 1][curr_cell.col]
                visit_cell.visited = True
                visited_cells.append(visit_cell)
                curr_cell = visit_cell
            elif dir == 2:
                # right
                visit_cell = self.maze[curr_cell.row ][curr_cell.col]
            elif dir == 3:
                # down
                pass
            elif dir == 4:
                # left
                run_alg = False
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

    def print_values(self):
        for row in self.maze:
            print('\nRow')
            for cell in row:
                print("[" + str(cell.cord.row) + "][" + str(cell.cord.col) + "]")
                if cell.wall_south and cell.wall_west:
                    print("Both walls")
                elif cell.wall_south:
                    print("Wall south")
                elif cell.wall_west:
                    print("Wall West")
                else:
                    print("----")

