#!/usr/bin/python

#primarily for annotation purposes
from graphtheory.structures.edges import Edge

try:
    from Queue import PriorityQueue
except ImportError:   # Python 3
    from queue import PriorityQueue
    xrange = range


class DijkstraMatrix:
    """The Dijkstra's algorithm with O(V**2) time.
    
    Attributes
    ----------
    graph : input directed weighted graph
    parent : dict with nodes (shortest path tree)
    distance : dict with nodes (distances to source node)
    source : node
    _in_queue : dict, private
    
    Examples
    --------
    >>> from graphtheory.structures.edges import Edge
    >>> from graphtheory.structures.graphs import Graph
    >>> from graphtheory.shortestpaths.dijkstra import DijkstraMatrix
    >>> G = Graph(n=10, True)    # an exemplary directed graph
    # Add nodes and edges here.
    >>> algorithm = DijkstraMatrix(G)   # initialization
    >>> algorithm.run(source)   # calculations
    >>> algorithm.parent   # shortest path tree as a dict
    >>> algorithm.distance[target]   # distance from source to target
    >>> algorithm.path(target)   # path from source to target
    
    Notes
    -----
    Based on:
    
    Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C., 2009, 
        Introduction to Algorithms, third edition, The MIT Press, 
        Cambridge, London.
    
    https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    """

    def __init__(self, graph):
        """The algorithm initialization.
        
        Parameters
        ----------
        graph : directed weighted graph with non-negative edge weights
        """
        if not graph.is_directed():
            raise ValueError("the graph is not directed")
        self.graph = graph
        # Shortest path tree as a dictionary.
        self.parent = dict((node, None) for node in self.graph.iternodes())
        self.distance = dict((node, float("inf")) for node in self.graph.iternodes())
        self.source = None
        self._in_queue = dict((node, True) for node in self.graph.iternodes())

    def run(self, source):
        """Finding shortest paths from the source.
        
        Parameters
        ----------
        source : node
        """
        self.source = source
        self.distance[source] = 0
        for _ in xrange(self.graph.v()):   # |V| times
            # Find min node, O(V) time.
            # Find the node with least distance, aka "cost"
            leastnode = min((node for node in self.graph.iternodes() 
                if self._in_queue[node]), key=self.distance.get)
            self._in_queue[leastnode] = False
            # Update (aka relax) those neigbours (via the edges) 
            for edge in self.graph.iteroutedges(node):   # O(V) time
                # that haven't been updated yet
                if self._in_queue[edge.target]:
                    self._relax(edge)

    def _relax(self, edge: Edge) -> bool: 
        """Edge relaxation."""
        alt = self.distance[edge.source] + edge.weight
        if self.distance[edge.target] > alt:
            # update the distance and parent
            self.distance[edge.target] = alt
            self.parent[edge.target] = edge.source
            return True
        return False

    def path(self, target) -> list:
        """Construct a path from source to target, recursively."""
        """returns a list containing the nodes"""
        if self.source == target:
            return [self.source]
        elif self.parent[target] is None:
            raise ValueError("no path to target")
        else:
            return self.path(self.parent[target]) + [target]


class Dijkstra(DijkstraMatrix):
    """The Dijkstra's algorithm for the shortest path problem.
    
    Attributes
    ----------
    graph : input directed weighted graph
    parent : dict with nodes (shortest path tree)
    distance : dict with nodes (distances to source node)
    source : node
    _in_queue : dict, private
    _pq : priority queue, private

    Examples
    --------
    >>> from graphtheory.structures.edges import Edge
    >>> from graphtheory.structures.graphs import Graph
    >>> from graphtheory.shortestpaths.dijkstra import DijkstraMatrix
    >>> G = Graph(n=10, True)    # an exemplary directed graph
    # Add nodes and edges here.
    >>> algorithm = DijkstraMatrix(G)   # initialization
    >>> algorithm.run(source)   # calculations
    >>> algorithm.parent   # shortest path tree as a dict
    >>> algorithm.distance[target]   # distance from source to target
    >>> algorithm.path(target)   # path from source to target
    
    Notes
    -----
    Based on:
    
    Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C., 2009, 
        Introduction to Algorithms, third edition, The MIT Press, 
        Cambridge, London.
    
    https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    """
    
    def __init__(self, graph):
        super().__init__(graph)
        self._pq = PriorityQueue()

    def run(self, source):
        """Finding shortest paths from the source.
        
        Parameters
        ----------
        source : node
        """
        self.source = source
        self.distance[source] = 0
        for node in self.graph.iternodes():
            self._pq.put((self.distance[node], node))
        while not self._pq.empty():
            _, node = self._pq.get()
            if self._in_queue[node]:
                self._in_queue[node] = False
            else:
                continue
            for edge in self.graph.iteroutedges(node):
                if self._in_queue[edge.target] and self._relax(edge):
                    self._pq.put((self.distance[edge.target], edge.target))


# EOF
