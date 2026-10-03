from nodes import Node, BranchNode, EndPointNode

class Cell():
    def __init__(self, length, width, x, y):
        """Initialises a cell with the given length, width, and x, y coordinates.
        Parameters:
          `length` (float): Cell length in cm
          `width` (float): Cell width in cm
          `x` (int): x coordinate
          `y` (int): y coordinate
        """
        self.length = length
        self.width = width
        self.x = x
        self.y = y
        self.has_node = False
        self.node = None
        self.node_type = None

    def add_node(self, node: Node | BranchNode | EndPointNode):
        if self.has_node:
            raise Exception("This Cell already contains a Node!")
        self.has_node = True
        self.node = node
        self.node_type = type(node)

    def remove_node(self):
        self.has_node = False

    def get_node(self):
        try:
            return type(self.node)
        except:
            raise Exception("This Cell does not contain a Node!")

    def get_node_type(self):
        try:
            return type(self.node)
        except:
            raise Exception("This Cell does not contain a Node!")