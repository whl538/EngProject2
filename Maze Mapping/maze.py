from enum import Enum

class Status(Enum):
    UNVISITED = 0
    VISITED = 1
    NODE = 2
    START = 3
    END = 4

class Cell():
    def __init__(self, x, y):
        """
        Initialise a cell at coordinates (x, y).
        """
        self.x = x
        self.y = y
        self.robot = False
        self.node = None
        self.status = Status.UNVISITED.value

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_coords(self):
        return (self.x, self.y)

    def set_robot(self):
        self.robot = not self.robot

    def has_robot(self):
        return self.robot

    def has_node(self):
        return bool(self.node)

    def add_node(self, id):
        if self.has_node():
            print("This cell already has a node!")
        else:
            self.node = id

    def get_node(self):
        return self.node

class Maze():
    def __init__(self, length, width, start_x=0, start_y=0):
        """
        Initialise a maze with the desired length and width. Represented as a 2D array.
        Optional parameters for an (x, y) coordinate of a starting position. Defaults to the top left corner
        """
        if start_x >= length or start_y >= width:
            raise ValueError("Your start point is out of bounds!")

        maze = []
        for i in range(length):
            row = []
            for j in range(width):
                row.append(Cell(j, i))
            maze.append(row)

        maze[start_y][start_x].set_status(Status.START.value)

        self.length = length
        self.width = width
        self.maze = maze

    def get_cell(self, x, y) -> Cell:
        """
        Gets the cell at coordinates (x, y)
        """
        return self.maze[y][x]

    def set_visited(self, x, y):
        """
        Sets the cell at coordinates (x, y) to visited.
        """
        self.get_cell(x, y).set_status(Status.VISITED.value)

    def add_node(self, x, y, id):
        """
        Sets the cell at coordinates (x, y) to a node.
        """
        cell = self.get_cell(x, y)
        cell.set_status(Status.NODE.value)
        cell.add_node(id)

    def set_end(self, x, y):
        """
        Sets the cell at coordinates (x, y) to be the end of the maze.
        """
        self.get_cell(x, y).set_status(Status.END.value)

    def is_visited(self, x, y):
        """
        Returns True if the cell at (x, y) is visited.
        """
        return self.get_cell(x, y).get_status() == Status.VISITED.value

    def is_node(self, x, y):
        """
        Returns True if the cell at (x, y) is a node.
        """
        return self.get_cell(x, y).has_node()

    def scan(self, x, y):
        """
        Scans surrounding cells (3x3 grid, with the cell at the centre, unless an edge cell).
        """
        scan = []

        # Check 4 corners
        if (x, y) == (0, 0):
            scan.append([self.maze[y][x], self.maze[y][x+1]])
            scan.append([self.maze[y+1][x], self.maze[y+1][x+1]])
        elif (x, y) == (self.length-1, 0):
            scan.append([self.maze[y][x-1], self.maze[y][x]])
            scan.append([self.maze[y+1][x-1], self.maze[y+1][x]])
        elif (x, y) == (0, self.width-1):
            scan.append([self.maze[y-1][x], self.maze[y-1][x+1]])
            scan.append([self.maze[y][x], self.maze[y][x+1]])
        elif (x, y) == (self.length-1, self.width-1):
            scan.append([self.maze[y-1][x-1], self.maze[y-1][x]])
            scan.append([self.maze[y][x-1], self.maze[y][x]])
        # Check edges
        elif x == 0:
            scan.append([self.maze[y-1][x], self.maze[y-1][x+1]])
            scan.append([self.maze[y][x], self.maze[y][x+1]])
            scan.append([self.maze[y+1][x], self.maze[y+1][x+1]])
        elif x == self.length-1:
            scan.append([self.maze[y-1][x-1], self.maze[y-1][x]])
            scan.append([self.maze[y][x-1], self.maze[y][x]])
            scan.append([self.maze[y+1][x-1], self.maze[y+1][x]])
        elif y == 0:
            scan.append([self.maze[y][x-1], self.maze[y][x], self.maze[y][x+1]])
            scan.append([self.maze[y+1][x-1], self.maze[y+1][x], self.maze[y+1][x+1]])
        elif y == self.width-1:
            scan.append([self.maze[y-1][x-1], self.maze[y-1][x], self.maze[y-1][x+1]])
            scan.append([self.maze[y][x-1], self.maze[y][x], self.maze[y][x+1]])
        else:
            scan.append([self.maze[y-1][x-1], self.maze[y-1][x], self.maze[y-1][x+1]])
            scan.append([self.maze[y][x-1], self.maze[y][x], self.maze[y][x+1]])
            scan.append([self.maze[y+1][x-1], self.maze[y+1][x], self.maze[y+1][x+1]])

        print("\n".join(str(row) for row in scan))

        return scan

    def is_explored(self):
        """
        Returns True if the maze is fully explored. False otherwise
        """
        for row in self.maze:
            for cell in row:
                if cell.get_status() == Status.UNVISITED.value:
                    return False
        return True

    def __str__(self):
        rows = [row for row in self.maze]
        return "\n".join(str(row) for row in rows)

if __name__ == "__main__":
    m = Maze(5, 5, 0, 4)

