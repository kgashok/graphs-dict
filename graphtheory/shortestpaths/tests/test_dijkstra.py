#!/usr/bin/python

import unittest
from graphtheory.structures.edges import Edge
from graphtheory.structures.graphs import Graph
from graphtheory.shortestpaths.dijkstra import Dijkstra, DijkstraMatrix

#    1
# 0 --> 1
# |   / |
# |5 /1 |3
# |./.  |.
# 2 --> 3
#    1

class TestDijkstra(unittest.TestCase):

    def setUp(self):
        self.N = 4           # number of nodes
        self.G = Graph(self.N, directed=True)
        self.nodes = range(self.N)
        self.edges = [
            Edge(0, 1, 1), Edge(0, 2, 5), Edge(1, 2, 1), Edge(1, 3, 3), 
            Edge(2, 3, 1)]
        for node in self.nodes:
            self.G.add_node(node)
        for edge in self.edges:
            self.G.add_edge(edge)
        #self.G.show()

    def test_shortest_path(self):
        print("Testing Dijkstra")
        source = 0
        target = 3
        algorithm = Dijkstra(self.G)
        algorithm.run(source)
        distance_expected = {0: 0, 1: 1, 2: 2, 3: 3}
        self.assertEqual(algorithm.distance, distance_expected)
        parent_expected = {0: None, 2: 1, 1: 0, 3: 2}
        self.assertEqual(algorithm.parent, parent_expected)
        path_expected = [0, 1, 2, 3]
        self.assertEqual(algorithm.path(target), path_expected)

    def test_dijkstra_matrix(self):
        print("Testing Dijkstra matrix")
        source = 0
        target = 3
        algorithm = DijkstraMatrix(self.G)
        algorithm.run(source)
        distance_expected = {0: 0, 1: 1, 2: 2, 3: 3}
        self.assertEqual(algorithm.distance, distance_expected)
        parent_expected = {0: None, 2: 1, 1: 0, 3: 2}
        self.assertEqual(algorithm.parent, parent_expected)
        path_expected = [0, 1, 2, 3]
        self.assertEqual(algorithm.path(target), path_expected)

    def test_dijkstra_for_path_not_found(self):
        print("Testing Matrix 2nd time")
        self.N = 8           # number of nodes
        self.G = Graph(self.N, directed=True)
        self.nodes = range(self.N)
        self.edges = [
            Edge(0, 1, 65), Edge(1, 8, 41), Edge(1, 2, 35),
            Edge(2, 3, 56), Edge(3, 4, 4),  Edge(3, 6, 20),
            Edge(5, 2, 30),
            Edge(6, 5, 18), Edge(6, 7, 15),
            Edge(8, 3, 28) 
        ]
        for node in self.nodes:
            self.G.add_node(node)
        for edge in self.edges:
            self.G.add_edge(edge)
        # self.G.show()
        
        algorithm = Dijkstra(self.G)
        source = 0
        algorithm.run(source)

        target = 7
        path_expected = [0, 1, 8, 3, 6, 7]
        distance_expected = 169
        self.assertEqual(path_expected, algorithm.path(target))
        self.assertEqual(distance_expected, algorithm.distance[target])

        algorithm2 = DijkstraMatrix(self.G)
        algorithm2.run(source)
        self.assertEqual(path_expected, algorithm.path(target))
        self.assertEqual(distance_expected, algorithm.distance[target])

        source = 2
        target = 8
        algorithm.run(source)
        try: 
            algorithm.path(target)
        except:
            pass
        else:
            self.fail("Path exception was not raised!")

        algorithm2.run(source)
        try: 
            algorithm2.path(target)
        except:
            pass
        else:
            self.fail("Path exception was not raised!")



    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
