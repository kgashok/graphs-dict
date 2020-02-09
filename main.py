from graphtheory.structures.edges import Edge
from graphtheory.structures.graphs import Graph
from graphtheory.planarity.planarfactory import PlanarGraphFactory

gf = PlanarGraphFactory(Graph)

G = gf.make_cyclic(n=10)      # cyclic topological graph
G = gf.make_wheel(n=10)       # wheel topological graph

G.show()
print ( G.v() )   # the number of nodes
print ( G.e() )   # the number of edges
print ( G.f() )   # the number of faces
for face in G.iterfaces():
    print ( face )


from alltests import run_all_tests
run_all_tests()