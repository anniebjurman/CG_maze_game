class Cell:
    def __init__(self):
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
        self.maze = [[Cell() for _ in range(size)] for _ in range(size)]

        self.cell_width = 1
    
    def set_cell(self, cell, wall):
        if wall == 'south':
            self.maze[cell[0]][cell[1]].wall_south = True
        elif wall == 'west':
            self.maze[cell[0]][cell[1]].wall_west = True
    
    def reset_maze(self):
        for row in self.maze:
            for cell in row:
                cell.reset_cell()
    
    def get_maze(self):
        return self.maze

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
