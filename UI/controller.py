from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAeroportoP = None
        self._choiceAeroportoA = None

    def handle_analizza_aeroporti(self, event):
        nMinStr = self._view._x_comp.value
        try:
            nMin = int(nMinStr)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire un numero intero nel campo 'compagnie minimo'"))
            self._view.update_page()
            return
        self._model.buildGraph(nMin)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo costruito con successo"))
        self._view._txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.getNumNodes()}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero archi: {self._model.getNumEdges()}"))
        self._view._ddAeroportoP.disabled = False
        self._view._btn_AeroportiConnessi.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btn_CercaItinerario.disabled = False
        self._view._numeroTratteMax.disabled = False
        self.fillDDAeroporti()
        self._view.update_page()

    def fillDDAeroporti(self):
        self._view._ddAeroportoP.options.clear()
        self._view._ddAeroportoA.options.clear()
        for a in self._model._nodi:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(
                    data=a,
                    on_click=self.readDDAeroportoP,
                    text=a.AIRPORT
            ))
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(
                    data=a,
                    on_click=self.readDDAeroportoA,
                    text=a.AIRPORT
            ))

    def readDDAeroportoP(self, event):
        if event.control.data is not None:
            self._choiceAeroportoP = event.control.data
        else:
            self._choiceAeroportoP = None
        print(f"Scelta aeroporto di partenza: {self._choiceAeroportoP}")

    def readDDAeroportoA(self, event):
        if event.control.data is not None:
            self._choiceAeroportoA = event.control.data
        else:
            self._choiceAeroportoA = None
        print(f"Scelta aeroporto di arrivo: {self._choiceAeroportoA}")

    def handle_aeroporti_connessi(self, event):
        v0 = self._choiceAeroportoP
        if v0 is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un aeroporto di partenza"))
            self._view.update_page()
            return
        vicini = self._model.findNeighbours(v0)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Aeroporti vicini a {v0}:"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    # Questo era richiesto nell'esercizio, non al punto 1 del tema d'esame
    def handle_test_connessione(self, event):
        v0 = self._choiceAeroportoP
        v1 = self._choiceAeroportoA
        if v0 is None or v1 is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un aeroporto di partenza e uno di arrivo"))
            self._view.update_page()
            return
        # Verificare se esiste un percorso tra i due aeroporti

        if not self._model.esistePercorso(v0, v1):
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Non esiste un percorso tra {v0} e {v1}"))
            self._view.update_page()
        else:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Esiste un percorso tra {v0} e {v1}"))
            self._view.update_page()

        # Trovare un possibile percorso tra i due aeroporti
        path = self._model.trovaCamminoBFS(v0, v1)
        self._view._txt_result.controls.append(
                ft.Text(f"Il cammino con minor numero di archi (BFS) tra {v0} e {v1} è:")
        )
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()

    def handle_cerca_itinerario(self, event):
        v0 = self._choiceAeroportoP
        v1 = self._choiceAeroportoA
        nMaxTratte = self._view._numeroTratteMax.value
        try:
            nMax = int(nMaxTratte)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un numero intero nel campo 'Numero tratte massimo'"))
            self._view.update_page()
            return
        tic = datetime.now()
        path, totCost = self._model.getBestItinerary(v0, v1, nMax)
        toc = datetime.now()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il percorso ottimo tra {v0} e {v1} compiute con {totCost} voli è:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view._txt_result.controls.append(ft.Text(f"Tempo impiegato per la ricerca: {toc - tic}"))
        self._view.update_page()
