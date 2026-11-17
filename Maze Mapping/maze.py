from enum import Enum

class Status(Enum):
    UNVISITED = 0
    VISITED = 1
    NODE = 2
    START = 3
    END = 4

class Maze():
    def __init__(self, length, width, start_x=0, start_y=0):
        """
        Initialise a maze with the desired length and width. Represented as a 2D array.
        Optional parameters for an (x, y) coordinate of a starting position. Defaults to the top left corner
        """
        if start_x >= length or start_y >= width:
            raise ValueError("Your start point is out of bounds!")

        maze = []
        for _ in range(length):
            row = []
            for _ in range(width):
                row.append(Status.UNVISITED.value)
            maze.append(row)

        maze[start_y][start_x] = Status.START.value

        self.length = length
        self.width = width
        self.maze = maze

    def set_visited(self, x, y):
        """
        Sets the cell at coordinates (x, y) to visited.
        """
        self.maze[y][x] = Status.VISITED.value

    def add_node(self, x, y):
        """
        Sets the cell at coordinates (x, y) to a node.
        """
        self.maze[y][x] = Status.NODE.value

    def set_end(self, x, y):
        """
        Sets the cell at coordinates (x, y) to be the end of the maze.
        """
        self.maze[x][y] = Status.END.value

    def is_visited(self, x, y):
        """
        Returns True if the cell at (x, y) is visited.
        """
        return self.maze[y][x] == Status.VISITED.value

    def is_node(self, x, y):
        """
        Returns True if the cell at (x, y) is a node.
        """
        return self.maze[y][x] == Status.NODE.value

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
            if 0 in row:
                return False
        return True

    def __str__(self):
        rows = [row for row in self.maze]
        return "\n".join(str(row) for row in rows)

if __name__ == "__main__":
    m = Maze(5, 5, 0, 4)

