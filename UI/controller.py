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

    def handle_cerca_itinerario(self, event):
        nMaxTratte = self._view._numeroTratteMax.value
        try:
            nMax = int(nMaxTratte)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire un numero intero nel campo 'Numero tratte massimo'"))
            self._view.update_page()
            return
        path, totCost = self._model.getBestItinerary(self._choiceAeroportoP, self._choiceAeroportoA, nMax)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Tratte compiute con {totCost} voli:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()

