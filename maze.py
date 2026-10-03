from nodes import Node, BranchNode, EndPointNode
from cell import Cell

class Maze():
    """The Maze is stored as a 2-Dimensional list of Cells"""
    def __init__(self, length, width, divisions):
        """Initialises the Maze with the given length, width, and number of cells per side
        Parameters:
          `length` (int): The Maze's length in cm
          `width` (int): The Maze's width in cm
          `divisions` (int): The number of cells per side of the maze
        """
        self.length = length
        self.width = width
        self.cell_length = length / divisions
        self.cell_width = width / divisions
        self.map = self.generate_map()

    def generate_map(self):
        cells = []
        for i in range(self.length):
            row = []
            for j in range(self.width):
                row.append(Cell(self.cell_length, self.cell_width, i, j))
            cells.append(row)

        return cells

    def get_cell(self, x, y) -> Cell:
        return self.map[x][y]

    def add_node(self, node: Node | BranchNode | EndPointNode, x, y):
        self.get_cell(x, y).add_node(node)

    def remove_node(self, x, y):
        self.get_cell(x, y).remove_node()

    def get_node_from_cell(self, x, y):
        ret = self.get_cell(x, y).get_node()

        if not ret:
            raise ValueError(f"There is no node in cell at {x}, {y}")
        return ret
        