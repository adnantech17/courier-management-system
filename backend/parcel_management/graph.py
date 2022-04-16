from collections import deque

INFINITY = float("inf")


class Graph:
    def __init__(self, data, start_node, end_node):
        print(start_node, end_node)
        graph_edges = []

        self.start_node = start_node
        self.end_node = end_node
        self.initial_processing_cost = 0

        for edge in data:
            graph_edges.append((edge.from_branch.id, edge.to_branch.id,
                               edge.shipping_cost + edge.to_branch.estimated_processing_cost))

            if edge.from_branch.id == start_node:
                self.initial_processing_cost = edge.from_branch.estimated_processing_cost

        print(graph_edges, self.initial_processing_cost)

        self.nodes = set()
        for edge in graph_edges:
            self.nodes.update([edge[0], edge[1]])

        self.adjacency_list = {node: set() for node in self.nodes}
        for edge in graph_edges:
            self.adjacency_list[edge[0]].add((edge[1], edge[2]))

    def shortest_path(self):
        unvisited_nodes = self.nodes.copy()
        distance_from_start = {
            node: (0 if node == self.start_node else INFINITY) for node in self.nodes
        }

        previous_node = {node: None for node in self.nodes}

        while unvisited_nodes:
            current_node = min(
                unvisited_nodes, key=lambda node: distance_from_start[node]
            )
            unvisited_nodes.remove(current_node)

            if distance_from_start[current_node] == INFINITY:
                break

            for neighbor, distance in self.adjacency_list[current_node]:
                new_path = distance_from_start[current_node] + distance
                if new_path < distance_from_start[neighbor]:
                    distance_from_start[neighbor] = new_path
                    previous_node[neighbor] = current_node

            if current_node == self.end_node:
                break
        path = deque()
        current_node = self.end_node
        while previous_node[current_node] is not None:
            path.appendleft(current_node)
            current_node = previous_node[current_node]
        path.appendleft(self.end_node)
        if distance_from_start[self.end_node] == INFINITY:
            cost = -1
        else:
            cost = distance_from_start[self.end_node] + \
                self.initial_processing_cost

        return path, cost
