import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self.DAO = DAO()
        self.lista_rifugi = []
        self._rifugi_dict = {}
        self._rifugi_dict_localita = {}


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO

        for rifugio in self.DAO.read_rifugio():
            self._rifugi_dict[rifugio.id] = rifugio.nome
            self._rifugi_dict_localita[rifugio.id] = rifugio.localita
        print(self._rifugi_dict)

        #print(self.DAO.read_connessioni(year))
        for connessione in self.DAO.read_connessioni(year):
            self.G.add_edge(connessione.id_rifugio1, connessione.id_rifugio2, weight = float(connessione.distanza) * connessione.difficolta)
            if connessione.id_rifugio1 not in self.lista_rifugi:
                self.lista_rifugi.append(connessione.id_rifugio1)
            if connessione.id_rifugio2 not in self.lista_rifugi:
                self.lista_rifugi.append(connessione.id_rifugio2)

        self.G.add_nodes_from(self.lista_rifugi)
        print(self.DAO.read_connessioni(year))
        print(self.G)


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        valori = []
        for arco in self.G.edges(data = True):
            valori.append(arco[2]["weight"])
        minimo = min(valori)
        massimo = max(valori)
        return minimo, massimo

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = 0
        maggiori = 0
        for arco in self.G.edges(data = True):
            if arco[2]["weight"] < soglia:
                minori += 1
            if arco[2]["weight"] > soglia:
                maggiori += 1
        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def get_cammino_minimo_ricorsivo(self, soglia : int):
        G_filtrato = nx.Graph()

        for u, v, data in self.G.edges(data = True):
            if data["weight"] > soglia:
                G_filtrato.add_edge(u,v, weight = data["weight"])


        percorso_minimo = None
        costo_minimo = float("inf")
        nodi = list(G_filtrato.nodes())

        for i in range(0, len(nodi)):
            for j in range(i + 1, len(nodi)):
                start = nodi[i]
                end = nodi[j]

                percorso, costo = self._ricorsione(start, end, G_filtrato, visitato = {start}, percorso = [start],costo = 0, best = (percorso_minimo, costo_minimo))
                if percorso is not None and costo < costo_minimo:
                    percorso_minimo = percorso[:] #per fare uan copia
                    costo_minimo = costo
        return percorso_minimo if percorso_minimo else []

    def _ricorsione(self, current, target, G_filtrato, visitato, percorso, costo, best):
        miglior_percorso, miglior_costo = best
        if costo >= miglior_costo:
            return best

        if current == target:
            if len(percorso) >= 3 and costo < miglior_costo:
                return (percorso[:], costo)  #copia senza modificare percorso
            return best

        for vicino in G_filtrato.neighbors(current):
            peso = G_filtrato[current][vicino]["weight"]
            if vicino not in visitato:
                percorso.append(vicino)
                visitato.add(vicino)
                best = self._ricorsione(vicino, target, G_filtrato, visitato, percorso, costo + peso, best)
                percorso.pop()
                visitato.remove(vicino)
        return best









