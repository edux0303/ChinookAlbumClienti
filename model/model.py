import networkx as nx
from database.DAO import DAO
from itertools import combinations


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._pesoBest = 0


    def buildGraph(self, nMin, nMax):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodi(nMin, nMax)
        for n in self._nodes:
            self.idMap[n.AlbumId] = n

        self._grafo.add_nodes_from(self._nodes)

        for idAlbum, venduti, incasso in DAO.getVendite():
            if idAlbum in self.idMap:
                self.idMap[idAlbum].venduti = venduti
                self.idMap[idAlbum].incasso = incasso

        for s1, s2 in DAO.getClientiAlbum():
            if s1 in self.idMap:
                self.idMap[s1].clienti.add(s2)

        for c1, c2 in combinations(self._nodes, 2):
            peso = len(c1.clienti & c2.clienti)
            if peso > 0:
                self._grafo.add_edge(c1, c2, weight=peso)

    def getNodes(self):
        return self._nodes

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)


    def getGradoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n) > self._grafo.degree(best):
                best = n
        return best, self._grafo.degree(best)

    def getPesoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n, weight="weight") > self._grafo.degree(best, weight="weight"):
                best = n
        return best, self._grafo.degree(best, weight="weight")

    def getComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        numero = len(componenti)
        piuGrande = 0
        for c in componenti:
            if len(c) > piuGrande:
                piuGrande = len(c)
        return numero, piuGrande

    def getTopArchi(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:5]


    def getNumSenzaVendite(self):
        conta = 0
        for album in self._nodes:
            if album.venduti == 0:
                conta += 1

        return conta

    def getIncassoMaxMin(self):
        venduti = []

        for album in sorted(self._nodes, key=str):
            if album.venduti > 0:
                venduti.append(album)

        if len(venduti) == 0:
            return None,None

        minimo = venduti[0]
        massimo = venduti[0]

        for album in venduti:
            if album.incasso > massimo.incasso:
                massimo = album
            if album.incasso < minimo.incasso:
                minimo = album
        return massimo, minimo


    def getGruppo(self,start,N):

        self._solBest = []
        self._pesoBest = -1

        self._maxIncasso = 0

        for album in self._nodes:
            if album.incasso > self._maxIncasso:
                self._maxIncasso = album.incasso

        self._ricorsione([start], start.incasso, N)

        return self._solBest, self._pesoBest


    def _ricorsione(self,parziale, incassoParziale, N):
        if len(parziale) == N:
            if incassoParziale > self._pesoBest:
                self._pesoBest = incassoParziale
                self._solBest = list(parziale)

            return

        mancanti = N - len(parziale)

        if incassoParziale + mancanti * self._maxIncasso <= self._pesoBest:
            return
        candidati = []
        for album in self._nodes:
            if self._ammissibile(album, parziale):
                candidati.append(album)

        candidati.sort(key=lambda x: -x.incasso)

        for c in candidati:
            parziale.append(c)
            self._ricorsione(parziale, incassoParziale+ c.incasso, N)
            parziale.pop()



    def _ammissibile(self,c,parziale):
        if c in parziale:
            return False
        conta = 0

        for p in parziale:
            if self._grafo.has_edge(c, p):
                conta += 1

        return conta == 1

