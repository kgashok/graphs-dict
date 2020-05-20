#!/usr/bin/python

import copy
import random
from graphtheory.structures.edges import Edge
try:
    integer_types = (int, long)
except NameError:   # Python 3
    integer_types = (int,)
    xrange = range

class Graph:
    """The class defining a graph.
    
    Graph class with list-of-list structure (the adjacency matrix
    representation). Nodes are int from 0 to n-1.
    """

    def __init__(self, n, directed=False):
        """Load up a Graph instance.
        
        Parameters
        ----------
        n : int (positive)
        directed : bool, optional (default=False)
        """
        if n < 1:
            raise ValueError("incorrect number of nodes")
        self.n = n
        self.directed = directed  # bool
        self.data = [[0] * self.n for node in xrange(self.n)]

    def is_directed(self):
        """Test if the graph is directed."""
        return self.directed

    def v(self):
        """Return the number of nodes (the graph order)."""
        return self.n

    def e(self):
        """Return the number of edges in O(V**2) time."""
        counter = 0
        for source in xrange(self.n):
            for target in xrange(self.n):
                if self.data[source][target] != 0:
                    counter += 1
        return (counter if self.is_directed() else counter // 2)

    def add_node(self, node):
        """Add a node to the graph."""
        if not isinstance(node, integer_types):
            raise ValueError("node is not int or long")
        if node >= self.n or node < 0:
            raise ValueError("node out of range")

    def has_node(self, node):
        """Test if a node exists."""
        if not isinstance(node, integer_types):
            raise ValueError("node is not int or long")
        if 0 <= node < self.n:
            return True
        else:
            return False

    def del_node(self, source):
        """Remove a node from the graph with edges.
        In fact, the node become isolated. It takes O(V) time."""
        for target in xrange(self.n):
            self.data[source][target] = 0
            self.data[target][source] = 0

    def add_edge(self, edge):
        """Add an edge to the graph."""
        if edge.source == edge.target:
            raise ValueError("loops are forbidden")
        self.add_node(edge.source)
        self.add_node(edge.target)
        if self.data[edge.source][edge.target] == 0:
            self.data[edge.source][edge.target] = edge.weight
        else:
            raise ValueError("parallel edges are forbidden")
        if not self.is_directed():
            if self.data[edge.target][edge.source] == 0:
                self.data[edge.target][edge.source] = edge.weight
            else:
                raise ValueError("parallel edges are forbidden")

    def del_edge(self, edge):
        """Remove an edge from the graph."""
        self.data[edge.source][edge.target] = 0
        if not self.is_directed():
            self.data[edge.target][edge.source] = 0

    def has_edge(self, edge):
        """Test if an edge exists (the weight is not checked)."""
        return self.data[edge.source][edge.target] != 0

    def weight(self, edge):
        """Return the edge weight or zero."""
        return self.data[edge.source][edge.target]

    def iternodes(self):
        """Generate the nodes from the graph on demand."""
        return iter(xrange(self.n))

    def iteradjacent(self, source):
        """Generate the adjacent nodes from the graph on demand."""
        for target in xrange(self.n):   # O(V) time
            if self.data[source][target] != 0:
                yield target

    def iteroutedges(self, source):   # O(V) time
        """Generate the outedges from the graph on demand."""
        for target in xrange(self.n):
            if self.data[source][target] != 0:
                yield Edge(source, target, self.data[source][target])

    def iterinedges(self, source):   # O(V) time
        """Generate the inedges from the graph on demand."""
        for target in xrange(self.n):
            if self.data[target][source] != 0:
                yield Edge(target, source, self.data[target][source])

    def iteredges(self):   # O(V**2) time
        """Generate the edges from the graph on demand."""
        for source in xrange(self.n):
            for target in xrange(self.n):
                if self.data[source][target] != 0 and (
                    self.is_directed() or source < target):
                    yield Edge(source, target, self.data[source][target])

    def show(self):
        """The graph presentation in O(V^2) time."""
        L = []
        for source in xrange(self.n):
            L.append("{} : ".format(source))
            for target in xrange(self.n):
                if self.data[source][target] == 1:
                    L.append("{} ".format(target))
                elif self.data[source][target] != 0:
                    L.append("{}({}) ".format(target, self.data[source][target]))
            L.append("\n")
        print("".join(L))

    def copy(self):
        """Return the graph copy in O(V**2) time."""
        new_graph = self.__class__(n=self.n, directed=self.directed)
        for source in xrange(self.n):
            for target in xrange(self.n):
                new_graph.data[source][target] = self.data[source][target]
        return new_graph

    def transpose(self):
        """Return the transpose of the graph in O(V**2) time."""
        new_graph = self.__class__(n=self.n, directed=self.directed)
        for source in xrange(self.n):
            for target in xrange(self.n):
                new_graph.data[source][target] = self.data[target][source]
        return new_graph

    def complement(self):
        """Return the complement of the graph."""
        new_graph = self.__class__(n=self.n, directed=self.directed)
        for source in xrange(self.n):
            for target in xrange(self.n):   # no loops
                if self.data[source][target] == 0 and source != target:
                    new_graph.data[source][target] = 1
        return new_graph

    def degree(self, source):
        """Return the degree of the node in the undirected graph."""
        if self.is_directed():
            raise ValueError("the graph is directed")
        counter = 0
        for target in xrange(self.n):
            if self.data[source][target] != 0:
                counter += 1
        return counter

    def outdegree(self, source):
        """Return the outdegree of the node."""
        counter = 0
        for target in xrange(self.n):
            if self.data[source][target] != 0:
                counter += 1
        return counter

    def indegree(self, source):
        """Return the indegree of the node."""
        counter = 0
        for target in xrange(self.n):
            if self.data[target][source] != 0:
                counter += 1
        return counter

    def __eq__(self, other):
        """Test if the graphs are equal."""
        if self.is_directed() is not other.is_directed():
            return False
        if self.v() != other.v():
            return False
        for source in xrange(self.n):   # time O(V**2)
            for target in xrange(self.n):
                if self.data[source][target] != other.data[source][target]:
                    return False
        return True

    def __ne__(self, other):
        """Test if the graphs are not equal."""
        return not self == other

    def add_graph(self, other):
        """Add a graph to this graph (the current graph is modified)."""
        if self.is_directed() is not other.is_directed():
            raise ValueError("directed vs undirected")
        if self.v() != other.v():
            raise ValueError("different numbers of nodes")
        for node in other.iternodes():
            self.add_node(node)
        for edge in other.iteredges():
            self.add_edge(edge)

    def save(self, file_name, name="Graph"):
        """Export the graph to the adjacency list format with comments."""
        afile = open(file_name, "w")
        afile.write("# NAME={}\n".format(name))
        afile.write("# DIRECTED={}\n".format(self.is_directed()))
        afile.write("# V={}\n".format(self.v()))
        afile.write("# E={}\n".format(self.e()))
        for edge in self.iteredges():
            if edge.weight == 1:
                afile.write("{} {}\n".format(edge.source, edge.target))
            else:
                afile.write("{} {} {}\n".format(edge.source, edge.target, edge.weight))
        afile.close()

    @classmethod
    def load(cls, file_name):
        """Import the graph from the adjacency list format with comments."""
        afile = open(file_name, "r")
        n = 1
        is_directed = False
        for line in afile:
            if line[0] == "#":
                if "# NAME=" in line:
                    name = line[7:-1]
                elif line == "# DIRECTED=False\n":
                    is_directed = False
                elif line == "# DIRECTED=True\n":
                    is_directed = True
                elif "# V=" in line:
                    n = int(line[4:-1])
                else:   # ignore other
                    graph = cls(n, is_directed)
            else:
                #alist = [int(x) for x in line.split()]
                alist = [eval(x) for x in line.split()]
                graph.add_edge(Edge(*alist))
        afile.close()
        return graph

    def save_lgl(self, file_name="graph.lgl"):
        """Export the graph to the adjacency list format (LGL)."""
        if self.is_directed():
            raise ValueError("the graph is directed")
        afile = open(file_name, "w")
        for edge in self.iteredges():
            if edge.weight == 1:
                afile.write("{} {}\n".format(edge.source, edge.target))
            else:
                afile.write("{} {} {}\n".format(edge.source, edge.target, edge.weight))
        afile.close()

    def save_ncol(self, file_name="graph.ncol"):
        """Export the graph to the labelled edge list format (NCOL)."""
        if self.is_directed():
            raise ValueError("the graph is directed")
        afile = open(file_name, "w")
        for node in self.iternodes():
            afile.write("# {}\n".format(node))
            for edge in self.iteroutedges(node):
                if edge.source < edge.target and edge.weight == 1:
                    afile.write("{}\n".format(edge.target))
                elif edge.source < edge.target:
                    afile.write("{} {}\n".format(edge.target, edge.weight))
        afile.close()

# EOF
