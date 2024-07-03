from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessioni import Connessione


class DAO():
    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from objects o"

        cursor.execute(query, ())  # non ha parametri

        for row in cursor:
            result.append(ArtObject(**row))  # li appendo in un oggetto di tipo ArtObject
            # **row al posto del costruttore lungo con ogni singolo parametro, questo lo posso fare perché
            # sto prendendo i dati come un dizionario, ma posso farlo SOLO SE i nomi della dataclass sono
            # esattamente gli stessi dei nomi della tabella, per questo non metto l'underscore _
            # equivalente a:
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(self, v1: ArtObject, v2: ArtObject):  # prende in ingresso due archi
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # con questa query ciclo due volte e ottengo il mio peso, il peso è dato da COUNT(*)
        query = """select count(*)   
            from exhibition_objects eo1, exhibition_objects eo2
            where eo1.exhibition_id = eo2.exhibition_id 
            and eo1.object_id < eo2.object_id 
            and eo1.object_id = %s
            and eo2.object_id = %s"""

        cursor.execute(query, (v1.object_id, v2.object_id))

        for row in cursor:
            result.append()

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni(idMap):  # metodo per prendere gli archi
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
            from exhibition_objects eo1, exhibition_objects eo2
            where eo1.exhibition_id = eo2.exhibition_id 
            and eo1.object_id < eo2.object_id 
            group by eo1.object_id, eo2.object_id
            order by peso desc"""

        cursor.execute(query, ())  # query non parametrica, quindi qua non ci metto nulla

        for row in cursor:
            result.append(Connessione(idMap[row["o1"]], idMap[row["o2"]], row["peso"]))
            # ad ogni ciclo di questo cursore creo un'istanza della classe Connessione in cui dico
            # il tuo primo nodo ha come id [row["o1"]] lo passo all'idMap e tiro fuori l'oggetto
            # il secondo nodo è [row["o2"]], e poi mi salvo il peso

        cursor.close()
        conn.close()
        return result
