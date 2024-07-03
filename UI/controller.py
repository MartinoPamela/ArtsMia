import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCercaPercorso(self, e):

        path, peso = self._model.getBestPath(int(self._view._ddLun.value),  # perché il dd mi restituisce una stringa
                                self._model.getObjFromId(int(self._view._txtIdOggetto.value)))

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato con peso migliore uguale a "
                                                       f"{peso}"))
        self._view._txt_result.controls.append(ft.Text(f"Percorso:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))

        self._view.update_page()

    def handleAnalizzaOggetti(self, e):
        self._model.creaGrafo()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi."))
        self._view.update_page()

    def handleCompConnessa(self,e):
        idAdded = self._view._txtIdOggetto.value

        try:
            intId = int(idAdded)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Il valore inserito non è un intero."))
            self._view.update_page()
            return
        # questo per controllare che l'utente abbia inserito effettivamente un intero

        # dopo questo devo verificare che l'id sia contenuto nel database
        if self._model.checkExistence(intId):  # quindi se esiste
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto {intId} è presente nel grafo."))
        else:
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto {intId} NON è presente nel grafo."))

        sizeConnessa = self._model.getConnessa(intId)  # qua mando il v0

        self._view._txt_result.controls.append(ft.Text(f"La componente connessa che contiene "
                                                       f"{intId} ha dimensione {sizeConnessa}."))

        # Fill DD
        # Dato che options si aspetta una lista di dropdown.Option, per riempire il dd ho due scelte:
        # o faccio un ciclo su myOpts e le aggiungo uno alla volta oppure mi faccio una lista di
        # questi oggetti qua, solitamente il primo modo perché è più facile da implementare

        self._view._ddLun.disabled = False
        self._view._btnCercaPercorso.disabled = False
        myOptsNum = list(range(2, sizeConnessa))  # questi saranno numeri
        self._view._ddLun.options = myOptsNum
        myOptsDD = list(map(lambda x: ft.dropdown.Option(x), myOptsNum))

        # map associa a un iterable una funzione, quindi gli do un iterable, una lista,
        # e map mi applica a ogni elemento di quella lista un metodo e mi restituisce in output una lista
        # in cui ha applicato quel metodo a quegli oggetti, metodo che può essere una lambda function

        # myOptsDD saranno oggetti che il mio DD si aspetta

        self._view._ddLun.options = myOptsDD

        # l'alternativa a list(map(lambda x: ft.dropdown.Option(x), myOptsNum)) è:
        # for i n range(2, sizeConnessa):
        #   self._view._ddLun.options.append(ft.dropdown.Option(i))

        self._view.update_page()


