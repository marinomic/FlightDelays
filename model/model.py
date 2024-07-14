import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._aeroporti = DAO.getAllAirports()
        self._idMap = {}
        for a in self._aeroporti:
            self._idMap[a.ID] = a
        self._nodi = None
        self._bestItinerary = []
        self._bestItineraryWeight = 0

    def buildGraph(self, x_compagnie):
        self._grafo.clear()
        self._nodi = DAO.getAllNodes(x_compagnie, self._idMap)
        self._grafo.add_nodes_from(self._nodi)
        self._addEdgesV2()

    def _addEdgesV1(self):
        allConnessioni = DAO.getAllEdgesV1(self._idMap)
        for c in allConnessioni:
            v0 = c.V0
            v1 = c.V1
            peso = c.N
            # Controllo che effettivamente esistano i nodi nel grafo, siccome
            # i nodi del grafo sono stati presi con una determinata condizione mentre
            # gli archi sono stati presi con un'altra condizione, qualsiasi arco, perciò non sono certo che siano tutti
            # archi di nodi presenti nel grafo
            if v0 in self._grafo and v1 in self._grafo:
                if self._grafo.has_edge(v0, v1):
                    self._grafo[v0][v1]['weight'] += peso
                else:
                    self._grafo.add_edge(v0, v1, weight=peso)

    def _addEdgesV2(self):
        allConnessioni = DAO.getAllEdgesV2(self._idMap)
        for c in allConnessioni:
            v0 = c.V0
            v1 = c.V1
            peso = c.N
            if v0 in self._grafo and v1 in self._grafo:
                self._grafo.add_edge(v0, v1, weight=peso)

    def getNumNodes(self):
        return len(self._grafo.nodes())

    def getNumEdges(self):
        return len(self._grafo.edges())

    def printGraphDetails(self):
        print(f"Numero nodi: {self.getNumNodes()},"
              f" numero archi: {self.getNumEdges()}")

    def findNeighbours(self, v0):
        """
        Alla pressione del bottone “Aeroporti connessi”, stampare l’elenco degli aeroporti adiacenti a quello selezionato,
        in ordine decrescente di numero totale di voli.
        """
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]['weight']))
        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple

        # oppure
        # vicini = self._grafo[v0]
        #         vicini = sorted(vicini.items(), key=lambda x: x[1]['weight'], reverse=True)
        #         return vicini

    def esistePercorso(self, aP, aA):
        connesse = nx.node_connected_component(self._grafo, aP)
        if aA in connesse:
            return True
        else:
            return False

    # Con Dijkstra troverò il cammino con peso minore tra due nodi
    def trovaCamminoDijkstra(self, aP, aA):
        return nx.dijkstra_path(self._grafo, aP, aA)

    # Con BFS troverò il cammino più corto tra due nodi, non necessariamente con peso minore
    def trovaCamminoBFS(self, aP, aA):
        tree = nx.bfs_tree(self._grafo, aP)
        # Costruiamo il cammino a partire da aA, quindi aP sarà l'ultimo elemento,
        # partiamo dalla foglia e risaliamo al nodo radice
        if aA in tree:
            print(f"{aA} è presente nell'albero di vista BFS")
        path = [aA]
        while path[-1] != aP:
            parent = list(tree.predecessors(path[-1]))[0]
            path.append(parent)
        # Perciò invertiamo il cammino
        path.reverse()
        return path

    # Con DFS troverò il cammino più lungo tra due nodi, non necessariamente con peso maggiore
    def trovaCamminoDFS(self, aP, aA):
        tree = nx.dfs_tree(self._grafo, aP)
        if aA in tree:
            print(f"{aA} è presente nell'albero di vista DFS")
        path = [aA]
        while path[-1] != aP:
            parent = list(tree.predecessors(path[-1]))[0]
            path.append(parent)

        path.reverse()
        return path

# Fatto da me in cui la ricorsione funziona e considera anche il caso in cui la soluzione ottimale venga raggiunta prima di aver compiuto
# il massimo di tratte, siccome si tratta di un massimo di tratte e non per forza di un numero di tratte necessario per il percorso richiesto.
#     def getBestItinerary(self, aP, aA, tratteMax):
#         """
#         Alla pressione del bottone“Cerca itinerario”, sviluppare un algoritmo ricorsivo agente sul grafo creato in
#         precedenza per cercare l’itinerario di viaggio tra v0 e v1 che massimizzi il numero totale di voli per ciascuna
#         delle tratte del percorso selezionato(in altre parole, il percorso che massimizzi la somma dei pesi degli archi attraversati),
#         utilizzando al massimo nMax tratte.
#         """
#         self._bestItinerary = []
#         self._bestItineraryWeight = 0
#         parziale = [aP]
#         for v in self._grafo.neighbors(aP):
#             parziale.append(v)
#             self.ricorsiva(parziale, aA, tratteMax)
#             parziale.pop()
#         return self._bestItinerary, self._bestItineraryWeight
#
#     def ricorsiva(self, parziale, target, tratteMax):
#         # caso terminale
#         if len(parziale) == tratteMax + 1 or parziale[-1] == target:
#             peso = self.calcolaPeso(parziale)
#             if peso > self._bestItineraryWeight:
#                 self._bestItinerary = copy.deepcopy(parziale)
#                 self._bestItineraryWeight = peso
#             return
#         # caso ricorsivo
#         ultimoNodo = parziale[-1]
#         for vicino in self._grafo.neighbors(ultimoNodo):
#             if vicino not in parziale:
#                 parziale.append(vicino)
#                 self.ricorsiva(parziale, target, tratteMax)
#                 parziale.pop()
#
#     def calcolaPeso(self, parziale):
#         peso = 0
#         for i in range(1, len(parziale)):
#             peso += self._grafo[parziale[i - 1]][parziale[i]]['weight']
#         return peso

# Fatto dal professore

    def getBestItinerary(self, aP, aA, tratteMax):
        self._bestItinerary = []
        self._bestItineraryWeight = 0
        parziale = [aP]
        # for v in self._grafo.neighbors(aP):
        #   parziale.append(v)
        self.ricorsiva(parziale, aA, tratteMax)
        #   parziale.pop()
        return self._bestItinerary, self._bestItineraryWeight

    def ricorsiva(self, parziale, target, tratteMax):
        # CASO TERMINALE
        # Verificare che parziale sia una soluzione ammissibile
        if len(parziale) == tratteMax + 1:
            return
        # Verificare se la soluzione trovata è migliore di quella attuale
        peso = self.calcolaPeso(parziale)
        if (peso > self._bestItineraryWeight
                and parziale[-1] == target):
            self._bestItinerary = copy.deepcopy(parziale)
            self._bestItineraryWeight = peso

        # CASO RICORSIVO
        # Posso ancora aggiungere nodi
        ultimoNodo = parziale[-1]  # ultimo nodo che ho aggiunto
        # Prendo i vicini dell'ultimo nodo e provo ad aggiungerli
        for vicino in self._grafo.neighbors(ultimoNodo):
            # Tipicamente qua inserisco dei vincoli, per esempio questo:
            if vicino not in parziale:
                # Ma nel nostro caso non è richisto dalla traccia alcun vincolo
                parziale.append(vicino)
                # Ricorsione
                self.ricorsiva(parziale, target, tratteMax)
                parziale.pop()

    def calcolaPeso(self, listOfNodes):
        peso = 0
        for i in range(1, len(listOfNodes)):
            peso += self._grafo[listOfNodes[i - 1]][listOfNodes[i]]['weight']
        return peso
