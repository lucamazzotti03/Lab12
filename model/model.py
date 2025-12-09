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


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO

        for rifugio in self.DAO.read_rifugio():
            self._rifugi_dict[rifugio.id] = rifugio.nome
        print(self._rifugi_dict)

        #print(self.DAO.read_connessioni(year))
        for connessione in self.DAO.read_connessioni(year):
            self.G.add_edge(connessione.id_rifugio1, connessione.id_rifugio2, weight = float(connessione.distanza) * connessione.difficolta)
            if connessione.id_rifugio1 not in self.lista_rifugi:
                self.lista_rifugi.append(connessione.id_rifugio1)
            if connessione.id_rifugio2 not in self.lista_rifugi:
                self.lista_rifugi.append(connessione.id_rifugio2)
        print(len(self.lista_rifugi))
        self.G.add_nodes_from(self.lista_rifugi)


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        valori = []
        for arco in self.G.edges(data = True):
            print(arco[2]["weight"])
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
