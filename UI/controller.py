import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def handleCreaGrafo(self, e):    # punto 1a/1b/1c
        self._view.txt_result.controls.clear()

        nMin = self._view._txtMin.value
        nMax = self._view._txtMax.value
        if nMin is None or nMin == "" or nMax is None or nMax == "":
            self._errore("Inserire il numero minimo e massimo di brani!")
            return
        try:
            nMin = int(nMin)
            nMax = int(nMax)
        except ValueError:
            self._errore("I due valori devono essere numeri interi!")
            return
        if nMin <= 0 or nMax <= 0:
            self._errore("I due valori devono essere maggiori di 0!")
            return
        if nMin > nMax:
            self._errore("Intervallo non valido: il minimo deve essere minore o uguale al massimo!")
            return

        self._model.buildGraph(nMin, nMax)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato per l'intervallo [{nMin}, {nMax}]!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._ddAlbum.options.clear()
        self._view._ddAlbum.value = None
        for a in sorted(self._model.getNodes(), key=str):
            self._view._ddAlbum.options.append(ft.dropdown.Option(key=str(a.AlbumId), text=str(a)))
        self._view.update_page()

    def handleStampaInfo(self, e):  # punto 1d
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        album, grado = self._model.getGradoMax()
        self._view.txt_result.controls.append(
            ft.Text(f"Album con grado maggiore: {album} (grado: {grado})"))

        album, somma = self._model.getPesoMax()
        self._view.txt_result.controls.append(
            ft.Text(f"Album con somma pesi incidenti massima: {album} (somma: {somma})"))

        numero, piuGrande = self._model.getComponenti()
        self._view.txt_result.controls.append(
            ft.Text(f"Componenti connesse: {numero} (la più grande ha {piuGrande} album)"))

        self._view.txt_result.controls.append(
            ft.Text(f"Album senza vendite: {self._model.getNumSenzaVendite()}"))

        massimo, minimo = self._model.getIncassoMaxMin()
        if massimo is None:
            self._view.txt_result.controls.append(ft.Text("Nessun album del grafo ha vendite."))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Album con incasso maggiore: {massimo} ({massimo.incasso:.2f})"))
            self._view.txt_result.controls.append(
                ft.Text(f"Album con incasso minore: {minimo} ({minimo.incasso:.2f})"))

        self._view.txt_result.controls.append(ft.Text("Top 5 archi con peso maggiore:"))
        i = 1
        for titolo1, titolo2, peso in self._model.getTopArchi():
            self._view.txt_result.controls.append(
                ft.Text(f"{i}. {titolo1} -- {titolo2} (peso: {peso})"))
            i += 1

        self._view.update_page()

    def handleGruppo(self, e):       # punto 2
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return
        if self._view._ddAlbum.value is None:
            self._errore("Selezionare un album!")
            return
        start = self._model.idMap.get(int(self._view._ddAlbum.value))
        if start is None:
            self._errore("Album non trovato!")
            return

        N = self._view._txtN.value
        if N is None or N == "":
            self._errore("Inserire il numero di album N!")
            return
        try:
            N = int(N)
        except ValueError:
            self._errore("N deve essere un numero intero!")
            return
        if N <= 0:
            self._errore("N deve essere maggiore di 0!")
            return
        if N > self._model.getNumNodi():
            self._errore("N è maggiore del numero di album nel grafo!")
            return

        gruppo, incassoTot = self._model.getGruppo(start, N)
        if len(gruppo) == 0:
            self._errore(f"Nessun gruppo di {N} album trovato a partire da '{start}'!")
            return

        self._view.txt_result.controls.append(ft.Text("Gruppo di album trovato:"))
        for a in sorted(gruppo, key=str):
            self._view.txt_result.controls.append(
                ft.Text(f"{a} - {a.venduti} brani venduti - incasso {a.incasso:.2f}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di album selezionati: {len(gruppo)}"))
        self._view.txt_result.controls.append(ft.Text(f"Incasso complessivo: {incassoTot:.2f}"))
        self._view.update_page()