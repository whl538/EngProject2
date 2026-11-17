from heapq import heapify, heappop, heappush
import json

class Graph:
    def __init__(self, graph: dict={}):
        """
        Initialises an empty graph with no shortest path
        """
        self.graph = graph
        self.shortest_path = []

    def load_graph_from_json(self, file_path):
        """
        Takes a json file and loads a graph
        """
        with open(file_path, "r") as f:
            self.graph = json.load(f)

    def load_path_fron_json(self, file_path):
        """
        Takes a json file and loads a path to take
        """
        with open(file_path, "r") as f:
            data = json.load(f)
            self.shortest_path = list(data.keys())

    def add_edge(self, node1, node2, weight, angle=0):
        """
        Adds an edge with the given weight and angle between node1 and node2
        """
        if node1 not in self.graph:  # Check if node is already added
            self.graph[node1] = {}  # If not, create node
        self.graph[node1][node2] = (weight, angle)  # Add connection to its neighbour
        self.graph[node2][node1] = (weight, -angle)  # Add reverse connection since the graph is not directed

    def get_shortest_distances(self, source: str):
        """
        Gets the shortest distances from the source node to all other nodes
        """
        # Initialise the values of all nodes to infinity
        distances = {node: float("inf") for node in self.graph}
        distances[source] = 0 # Set the source value to 0

        # Initialise a dictionary to store path
        predecessors = {node: None for node in self.graph}

        # Initialise a priority queue
        pq = [(0, source)]
        heapify(pq)

        # Create a set to hold visited nodes
        visited = set()

        while pq:
            current_distance, current_node = heappop(pq)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbour, (weight, _) in self.graph[current_node].items():
                # Calculate the distance from current_node to its neighbour
                neighbour_distance = current_distance + weight
                if neighbour_distance < distances[neighbour]:
                    distances[neighbour] = neighbour_distance
                    heappush(pq, (neighbour_distance, neighbour))

        # Construct the path
        for node, distance in distances.items():
            for neighbour, (weight, _) in self.graph[node].items():
                if distances[neighbour] == distance + weight:
                    predecessors[neighbour] = node

        return distances, predecessors

    def get_shortest_path(self, source: str, target: str):
        """
        Gets the shortest path from source to target
        """
        # Generate the predecessors dict
        _, predecessors = self.get_shortest_distances(source)

        path = []
        current_node = target

        # Backtrack from the current node using predecessors
        while current_node:
            path.append(current_node)
            current_node = predecessors[current_node]

        # Reverse the path and return it
        path.reverse()

        self.shortest_path = path
        return path

    def write_graph_json(self, file_path):
        """
        Writes the graph to a json.
        """
        try:
            json_str = json.dumps(self.graph, indent=4)
            with open(file_path, "w") as f:
                f.write(json_str)
            print(f"Successfully dumped {file_path}!")
        except:
            print(f"Error dumping {file_path}!")


    def write_path_json(self, file_path):
        """
        Writes information (nodes, distances, and angles) about the last saved path to a json.
        """
        shortest_path_dict = {}
        for i, node in enumerate(self.shortest_path):
            distance, angle = (0, 0)
            if i != len(self.shortest_path) - 1:
                distance, angle = self.graph[node][self.shortest_path[i+1]]
            shortest_path_dict[node] = {"Distance": distance, "Angle": angle}

        try:
            json_str = json.dumps(shortest_path_dict, indent=4)
            with open(file_path, "w") as f:
                f.write(json_str)
            print(f"Successfully dumped {file_path}!")
        except:
            print(f"Error dumping {file_path}!")



if __name__ == "__main__":
    graph = {
             "A": {"B": (3, 70), "C": (3, 40)},
             "B": {"A": (3, 0), "D": (3.5, 90), "E": (2.8, -90)},
             "C": {"A": (3, 90), "E": (2.8, 0), "F": (3.5, 0)},
             "D": {"B": (3.5, 90), "E": (3.1, 0), "G": (10, 0)},
             "E": {"B": (2.8, 60), "C": (2.8, 30), "D": (3.1, 20), "G": (7, 0)},
             "F": {"G": (2.5, 65), "C": (3.5, 40)},
             "G": {"F": (2.5, 180), "E": (7, 60), "D": (10, 50)},
    }

    G = Graph(graph)
    F = Graph()

    F.load_graph_from_json("graph.json")
    F.load_path_fron_json("path.json")

    print(F.graph)
    print(F.shortest_path)

    print(F.get_shortest_path("B", "F"))