class Node():
    """Base Node class, upon which other node types are built."""
    def __init__(self, id, x, y):
        """Initialises a new base Node. All nodes have an ID, as well as an x and y coordinate
        Parameters:
          `id` (any): Unique id of the Node
          `x` (int): x coordinate of the Node
          `y` (int): y coordinate of the Node
        """
        self.id = id
        self.parent = None
        self.children = []
        self.value = None
        self.location = (x, y)

    def set_value(self, value):
            self.value = value
    
    def get_value(self):
        if not self.value:
            raise ValueError('This Node does not have a value!')
        return self.value

    def get_location(self):
        """Returns the x and y coordinate of the Node as a tuple"""
        return self.location

class BranchNode(Node):
    """Branch Nodes are Nodes with both a parent and at least one child"""
    def __init__(self, id, x, y, distance):
        """Initialises a new Branch Node. Branch nodes have an ID, x and y coordinate, and a distance from their parent
        Parameters:
                  `id` (any): Unique id of the Node
                  `x` (int): x coordinate of the Node
                  `y` (int): y coordinate of the Node
                  `distance` (float): distance of the node from its parent
        """
        super().__init__(id, x, y)
        self.calculated = False
        self.distance_from_parent = distance

    def get_distance_from_parent(self):
        return self.distance_from_parent

    def add_child(self, child: Node):
        self.children.append(child)

    def remove_child(self, child: Node):
        self.children.remove(child)

    def set_parent(self, parent: Node):
        self.parent = parent

    def get_parent(self, parent: Node):
        return self.parent

    def toggle_calculated(self):
        self.calculated = not self.calculated

    def is_calculated(self):
        return self.calculated

    def __str__(self):
        return f'''Branch Node {self.id}:\n\tLocation: {self.location}\n\tCalculated: {self.calculated}'''

class EndPointNode(BranchNode):
    """End Point Nodes are Nodes with either a parent or at least one child, but not both"""
    def __init__(self, id, x, y, distance=None):
        """Initialises a new End Point Node. End Point nodes have an ID, x and y coordinate, and possibly a distance from their parent
        Parameters:
          `id` (any): Unique id of the Node
          `x` (int): x coordinate of the Node
          `y` (int): y coordinate of the Node
          `distance` (float): distance of the node from its parent (default = None)
        """
        super().__init__(id, x, y, distance)
        self.start = False
        self.end = False

    def toggle_start(self):
        self.start = not self.start

    def toggle_end(self):
        self.end = not self.end

    def is_start(self):
        return self.start

    def is_end(self):
        return self.end

    def __str__(self):
        return f'''End Point Node {self.id}:\n\tStart: {self.start}\n\t End: {self.end}'''

if __name__ == "__main__":
    test_branch = BranchNode(1, 0, 0, 5)
    test_end = EndPointNode(2, 0, 1)

    print(str(test_branch))
    print(str(test_end))