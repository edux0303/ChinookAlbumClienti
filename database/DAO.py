from database.DB_connect import DBConnect
from model.album import Album


"""
CHINOOK: ALBUM E CLIENTI

Si consideri il database "Chinook", contenente informazioni, fra le altre cose,
su album (album), brani (track), fatture (invoice) e righe di fattura
(invoiceline). Ogni album contiene uno o piu' brani, ogni riga di fattura si
riferisce a un brano e ogni fattura e' intestata a un cliente.
Si intende costruire un'applicazione che permetta di analizzare le relazioni tra
album in base ai clienti che ne hanno acquistato i brani.

PUNTO 1
a. L'utente inserisce in due campi di testo un numero minimo e un numero massimo
   di brani, che definiscono l'intervallo [n_min, n_max]. I due campi devono
   mostrare come valori di default 12 e 14.

b. Premendo "Crea grafo", l'applicazione costruisce un grafo semplice, non
   orientato e pesato. I vertici sono gli album che contengono un numero di
   brani (tabella track) compreso nell'intervallo, estremi inclusi.
   SUGGERIMENTO. Per ogni album puo' risultare conveniente aggiungere alla
   relativa classe:
   - il numero di brani venduti, cioe' la somma di Quantity nelle righe di
     fattura dei suoi brani;
   - l'incasso, cioe' la somma di UnitPrice * Quantity nelle stesse righe;
   - l'insieme dei clienti che hanno acquistato almeno un suo brano.
   NOTA. Non tutti gli album hanno venduto brani. Gli album senza vendite fanno
   comunque parte del grafo, con brani venduti e incasso pari a zero, e restano
   isolati.

c. Esiste un arco tra due album distinti A1 e A2 se almeno un cliente ha
   acquistato brani di entrambi. Il peso dell'arco e' il numero di clienti
   distinti in comune. Costruito il grafo, l'applicazione visualizza il numero
   di vertici e di archi.

d. Alla pressione del tasto "Stampa Info", l'applicazione visualizza:
   - l'album con grado maggiore;
   - l'album con la somma dei pesi degli archi incidenti massima;
   - il numero di componenti connesse e la dimensione della piu' grande;
   - il numero di album senza vendite;
   - l'album con incasso maggiore e quello con incasso minore, considerando
     solo gli album che hanno venduto almeno un brano; se nessun album del
     grafo ha vendite, va mostrato un messaggio, senza generare eccezioni;
   - i 5 archi di peso maggiore, in ordine decrescente di peso; in caso di
     parita', ordinamento alfabetico sul titolo del primo album e poi del
     secondo.
   In caso di parita' nei punti con un solo album si scelga il primo in ordine
   alfabetico di titolo.

PUNTO 2
a. L'utente seleziona da un menu a tendina un album di partenza tra quelli
   presenti nel grafo, e inserisce in un campo di testo un valore intero
   positivo N.

b. Premendo "Trova gruppo album", l'applicazione determina, mediante un
   algoritmo ricorsivo, un insieme di album che soddisfi questi vincoli:
   - il gruppo contiene esattamente N album;
   - il primo album del gruppo e' quello scelto dall'utente;
   - ogni album aggiunto dopo il primo deve essere adiacente a esattamente un
     album gia' presente nel gruppo (non a zero, ne' a due o piu'): il gruppo
     cresce cioe' formando una struttura ad albero;
   - tra tutte le soluzioni ammissibili, va trovata quella che massimizza
     l'incasso complessivo degli album selezionati.

c. L'applicazione stampa:
   - la lista degli album selezionati, ordinata alfabeticamente;
   - per ciascun album, il numero di brani venduti e l'incasso;
   - il numero totale di album selezionati;
   - l'incasso complessivo della soluzione ottima.
   Se non esiste nessun gruppo ammissibile, va mostrato un messaggio.

Tutti i possibili errori di immissione, validazione dati, accesso al database
ed algoritmici devono essere gestiti; non sono ammesse eccezioni generate dal
programma.

VALORI DI CONTROLLO
Punto 1
- 12-14: 79 vertici, 705 archi
    grado maggiore: The Best Of 1980-1990 (38)
    somma pesi massima: The Best Of 1980-1990 (47)
    componenti connesse: 1 (la piu' grande di 79)
    album senza vendite: 0
    incasso maggiore: American Idiot (14.85); minore: Carry On (3.96)
    top 5 archi, tutti di peso 4:
      1. Album Of The Year -- Angel Dust
      2. Alcohol Fueled Brewtality Live! [Disc 1] -- BackBeat Soundtrack
      3. Alcohol Fueled Brewtality Live! [Disc 1] -- Out Of Exile
      4. As Cancoes de Eu Tu Eles -- The Colour And The Shape
      5. Audioslave -- Warner 25 Anos
- 18-30: 31 vertici, 203 archi
    grado maggiore: Unplugged (22)
    somma pesi massima: Unplugged (37)
    componenti connesse: 1 (la piu' grande di 31)
    album senza vendite: 0
    incasso maggiore: Battlestar Galactica (Classic), Season 1 (35.82)
    incasso minore: Barulhinho Bom (7.92)
    top 5 archi:
      1. The Cream Of Clapton -- Unplugged (5)
      2. Battlestar Galactica, Season 3 -- Heroes, Season 1 (4)
      3. Heroes, Season 1 -- Lost, Season 3 (4)
      4. Lost, Season 1 -- Lost, Season 2 (4)
      5. Acustico MTV -- Afrociberdelia (3)
- 1-5: 97 vertici, 113 archi
    grado maggiore: The Song Remains The Same (Disc 2) (12)
    somma pesi massima: The Song Remains The Same (Disc 2) (12)
    componenti connesse: 54 (la piu' grande di 18)
    album senza vendite: 43
    incasso maggiore: Aquaman (3.98)
    incasso minore: Adams, John: The Chairman Dances (0.99)
- 13-13: 16 vertici, 23 archi
    grado maggiore: American Idiot (8)
    somma pesi massima: American Idiot (9)
    componenti connesse: 3 (la piu' grande di 14)
- 14-12, oppure un campo vuoto o con lettere: messaggio di errore
- 100-200: 0 vertici, 0 archi, senza errori

Punto 2
- 18-30, Greatest Kiss, N = 3 -> incasso 87.46
- 18-30, Greatest Kiss, N = 4 -> incasso 107.36
    (Battlestar Galactica (Classic), Season 1; Greatest Kiss;
     Heroes, Season 1; Lost, Season 2)
- 18-30, Greatest Kiss, N = 5 -> incasso 132.14
- 12-14, Achtung Baby, N = 4 -> incasso 47.52
- 13-13, Alcohol Fueled Brewtality Live! [Disc 1], N = 3 -> incasso 31.68
- 1-5, A Copland Celebration, Vol. I, N = 3 -> nessun gruppo (album isolato)

"""

class DAO():
    def __init__(self):
        pass

    # ---------- 1b: vertici (album con numero di brani nell'intervallo) ----------
    @staticmethod
    def getNodi(nMin, nMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT al.AlbumId AS id, al.Title AS titolo, COUNT(*) AS numBrani
                FROM album al, track t
                WHERE al.AlbumId = t.AlbumId 
                GROUP BY al.AlbumId, al.Title
                HAVING COUNT(*) BETWEEN %s AND %s
        """
        cursor.execute(query, (nMin, nMax))
        for row in cursor:
            result.append(Album(row["id"], row["titolo"], int(row["numBrani"])))
        cursor.close()
        cnx.close()
        return result

    # ---------- 1b: brani venduti e incasso di ogni album ----------
    @staticmethod
    def getVendite():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT t.AlbumId AS id, SUM(il.Quantity) AS venduti, SUM(il.Quantity * il.UnitPrice) AS incasso
        FROM track t, invoiceline il
        WHERE t.TrackId = il.TrackId
        GROUP BY t.AlbumId
        """
        cursor.execute(query)
        for row in cursor:
            result.append((row["id"], int(row["venduti"]), float(row["incasso"])))
        cursor.close()
        cnx.close()
        return result

    # ---------- 1c: clienti che hanno acquistato ogni album ----------
    @staticmethod
    def getClientiAlbum():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
        SELECT DISTINCT t.AlbumId AS idAlbum, i.CustomerId AS idCliente
        FROM invoice i, invoiceline il, track t
        WHERE il.invoiceId = i.InvoiceId AND il.TrackId = t.TrackId
        """
        cursor.execute(query)
        for row in cursor:
            result.append((row["idAlbum"], row["idCliente"]))
        cursor.close()
        cnx.close()
        return result