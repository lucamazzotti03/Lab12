from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    def read_rifugio(self):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        cursor.execute('''SELECT * FROM rifugio''')
        for row in cursor:
            rifugio = Rifugio(row["id"], row["nome"], row["localita"], row["altitudine"], row["capienza"], row["aperto"])
            result.append(rifugio)

        conn.close()
        cursor.close()
        return result


    def read_connessioni(self, anno : int):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = '''SELECT * FROM connessione WHERE anno <= %s'''
        cursor.execute(query, (anno,))
        for row in cursor:

            difficolta = row["difficolta"]
            if difficolta == "facile":
                difficolta = 1
            elif difficolta == "media":
                difficolta = 1.5
            elif difficolta == "difficile":
                difficolta = 2

            result.append(Connessione(row["id"], row["id_rifugio1"], row["id_rifugio2"], row["distanza"], difficolta, row["durata"], row["anno"]))

        #print(result)
        conn.close()
        cursor.close()
        return result
