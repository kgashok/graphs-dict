from graphtheory.structures.edges import Edge
from graphtheory.structures.graphs import Graph
from graphtheory.planarity.planarfactory import PlanarGraphFactory

gf = PlanarGraphFactory(Graph)

G = gf.make_cyclic(n=10)      # cyclic topological graph
G = gf.make_wheel(n=10)       # wheel topological graph

# G.show()
print ( G.v() )   # the number of nodes
print ( G.e() )   # the number of edges
print ( G.f() )   # the number of faces
for face in G.iterfaces():
    print ( face )


'''
from alltests import run_all_tests
run_all_tests()
'''


from graphtheory.structures.graphs import Graph
from graphtheory.structures.factory import GraphFactory

gf = GraphFactory(Graph)
G = gf.make_random(n=10, directed=True)
G.show()
from pprint import pprint 
pprint(G)

from graphtheory.shortestpaths.dijkstra import Dijkstra
algo = Dijkstra(G)
source = 5 
algo.run(source)

# get results 
target = 8
print(algo.path(target), algo.distance[target])