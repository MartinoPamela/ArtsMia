import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._artObjectList = DAO.getAllObjects()  # metto nella lista gli oggetti
        # lo faccio nell'init del modello perché gli oggetti non cambieranno durante
        # l'esecuzione del programma, perché sono tuti gli oggetti
        self._grafo = nx.Graph()  # grafo non orientato è un grafo di tipo Graph
        self._grafo.add_nodes_from(self._artObjectList)
        self._idMap = {}  # dizionario
        for v in self._artObjectList:
            self._idMap[v.object_id] = v  # questo dizionario mi serve ad associare l'id dell'oggetto all'oggetto
        self._solBest = []
        self._pesoBest = 0

    def getBestPath(self, lun, v0):
        self._solBest = []  # mi assicuro di partire con tutto pulito
        self._pesoBest = 0

        parziale = [v0]  # lista vuota inizialmente ma già qui so che ci posso mettere v0

        for v in self._grafo.neighbors(v0):  # così mi assicuro di entrare in ricorsione con una lista lunga almeno 2
            if v.classification == v0.classification:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()

        return self._solBest, self._pesoBest

    def ricorsione(self, parziale, lun):  # se arrivo con una lista lunga 1 non ho un peso che mi posso calcolare

        # controllo se parziale è una sol valida col primo if, ed in caso se è migliore del best col secondo if
        if len(parziale) == lun:  # verifico che questa sia una soluzione migliore di quella che ho trovato finora
            if self.peso(parziale) > self._pesoBest:
                self._pesoBest = self.peso(parziale)
                self._solBest = copy.deepcopy(parziale)
            return  # esco perché non ha senso continuare ad aggiungere elementi

        # se arrivo qui, allora len(parziale) < lun, quindi ha senso continuare ad aggiungere
        for v in self._grafo.neighbors(parziale[-1]):  # ultimo elemento di parziale
            # v lo aggiungo se non è già in parziale e poi mi devo assicurare che abbia la stessa classification di v0
            if v.classification == parziale[-1].classification and v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()
                # quando esco da questo for vuol dire che ho finito

    def peso(self, listObject):  # è una lista di oggetti che sono sicura che sono collegati da un arco che li collega
        # perché li sto aggiungendo tramite vicini, quindi sono sicura che gli elementi
        # successivi della lista hanno sicuramente un arco che avrà un peso

        p = 0

        for i in range(0, len(listObject)-1):  # -1 perché devo contare gli archi, e devo arrivare all'ultimo elemento
            p += self._grafo[listObject[i]][listObject[i+1]]["weight"]
            # oggetto in posizione 0 e oggetto in posizione 1 e così via

        # qui sto sfruttando il fatto che per costruzione della mia lista di oggetti che arriva
        # in questo metodo è collegato ad archi, mi prendo gli archi successivi e mi sommo quei pesi

        return p

    def getConnessa(self, v0int):  # v0int è un argomento del metodo, ed è il nodo da cui partire
        """
        quando mi chiede la componente connessa il Depth First Search è una buona soluzione per trovare le componenti
        connesse, perché io parto da un nodo e trovo tutti i nodi che sono connessi a quel nodo lì, che di fatto è la
        definizione di componente connessa. Dato che qui mi chiede di stampare i nodi è inutile ciclare sugli archi,
        dfs_edges mi restituisce gli archi dell'albero di visita,quindi uso dfs_tree che mi recupera direttamente
        l'albero di visita, o dfs_predecessors o dfs_successors che mi danno l'esplorazione che l'algoritmo sta facendo
        """

        v0 = self._idMap[v0int]  # v0 è un intero, ma io vorrei v0 nodo, così lo riconverto in oggetto

        # MOODO 1: successori di v0 in DFS
        successors = nx.dfs_successors(self._grafo, v0)  # l'output di questo algoritmo è un dizionario che ha
        # come chiave un nodo e ocme valore tutti i noidi dove ci puoi arrivare, quindi
        # tutti gli archi che escono da quel nodo lì, e da un nodo puoi andare in più punti
        allSucc = []
        for v in successors.values():
            # allSucc.append(v)
            # append si aspetta un oggetto, quindi aggiunge un elemento, quindi se gli aggiungi
            # una lista ti aggiunge un elemento alla lista che contiene la lista
            allSucc.extend(v)
            # extend fa l'unpack della lista che gli passi in ingresso, e aggiunge i singoli
            # elementi, quindi cicla sugli elementi di v e li aggiunge uno per uno

        print(f"Metodo 1 (pred): {len(allSucc)}")  # mi dice la dimensione di questa componente connessa

        # MODO 2: predecessori di v0 in DFS, che sarebbe l'algoritmo che va al contrario perché il grafo non è
        # orientato, quindi predecessori e successori è la stessa cosa
        predecessors = nx.dfs_predecessors(self._grafo, v0)  # predecessors è l'arco da cui sei arrivato
        # ed è sempre unico nell'esplorazione
        print(f"Metodo 2 (succ): {len(predecessors.values())}")

        # MODO 3: recupero l'albero di visita del DFS e conto i nodi
        tree = nx.dfs_tree(self._grafo, v0)  # tree è un grafo
        print(f"Metodo 3 (tree): {len(tree.nodes)}")

        # MODO 4: node_connected_component
        connComp = nx.node_connected_component(self._grafo, v0)  # questo metodo restituisce un set di nodi
        print(f"Metodo 4 (connected comp): {len(connComp)}")

        return len(connComp)


    def creaGrafo(self):
        self.addEdges()

    def addEdges(self):

        # Soluzione 1: ciclare sui nodi
        # alternativa sconsigliata (faccio tante query quindi è più lento) conviene solo con grafi piccoli
        # soluzione più semplice dal punto di vista della programmazione ma è più lenta
        # for u in self._artObjectList:
        #    for v in self._artObjectList:
        #        peso = DAO.getPeso(u, v)
        #        self._grafo.add_edge(u, v, weight=peso)

        # Soluzione 2: una sola query
        # ricavare già tutti gli archi
        allEdges = DAO.getAllConnessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.v1, e.v2, weight=e.peso)

    def checkExistence(self, idOggetto):
        return idOggetto in self._idMap  # mi verifica se idOggetto è contenuto nelle chiavi del mio dizionario
        # quindi mi restituirà True se l'idOggetto esiste, False altrimenti

    def getObjFromId(self, idOggetto):
        return self._idMap[idOggetto]
        # perché io l'idMap, quindi il mio dizionario di oggetti, ce l'ho solo nel modello, quindi nel
        # controller in teoria non potrei averci accesso, però se mi faccio un metodo che mi restiuisce
        # questo oggetto poi posso usarlo dal controller

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    """
    Testo ricorsione: 
    a. Permettere all'utente di inserire, in una seconda casella di testo, un numero intero, detto LUN,
       compreso tra 2 e la dimensione della componente connessa relativa al vertice selezionato al punto 1c.
    b. Alla pressione del bottone "Cerca oggetti", il programma dovrà cercare il cammino di peso massimo,
       avente lunghezza pari a LUN, il cui vertice iniziale coincida con il vertice selezionato nel
       punto 1c, che comprenda esclusivamente vertici che abbiano tutti la stessa classification.
    c. Al termine della ricerca, il programma dovrà stampare il cammino, indicando gli oggetti incontrati
       (ordinati per object_name) ed il peso totale del cammino trovato.
    """
