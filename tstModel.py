from datetime import datetime

import networkx as nx

from model.model import Model

mymodel = Model()
mymodel.buildGraph(5)
mymodel.printGraphDetails()

v0 = mymodel._nodi[0]
connessa = list(nx.node_connected_component(mymodel._grafo, v0))
v1 = connessa[10]

pathDijkstra = mymodel.trovaCamminoDijkstra(v0, v1)
pathBFS = mymodel.trovaCamminoBFS(v0, v1)
pathDFS = mymodel.trovaCamminoDFS(v0, v1)

print("-------------------")
print("Metodo di Dijkstra")
print(*pathDijkstra, sep=" \n")
print("-------------------")
print("Metodo albero Breadth first")
print(*pathBFS, sep="\n")
print("------------------")
print("Metodo albero Depth first")
print(*pathDFS, sep="\n")

tic = datetime.now()
bestPath, bestScore = mymodel.getBestItinerary(v0, v1, 4)
toc = datetime.now()
print("------------------")
print(f"Cammino ottimo tra {v0} e {v1} dal peso di {bestScore} trovato in {toc - tic}")
print(*bestPath, sep="\n")
