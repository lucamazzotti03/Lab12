from dataclasses import dataclass


@dataclass
class Connessione:
    id : int
    id_rifugio1 : int
    id_rifugio2 : int
    distanza : int
    difficolta : str
    durata : int
    anno : int

#
    def __str__(self):
        return f"{self.id} {self.id_rifugio1} {self.id_rifugio2} {self.distanza} {self.difficolta} {self.durata} {self.anno}"

    def __hash__(self):
        return hash(self.id)