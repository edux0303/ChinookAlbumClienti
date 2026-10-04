from dataclasses import dataclass, field


@dataclass
class Album:
    AlbumId: int
    Title: str
    numBrani: int                                 # brani contenuti nell'album
    venduti: int = 0                              # brani venduti
    incasso: float = 0.0                          # somma di UnitPrice * Quantity
    clienti: set = field(default_factory=set)     # id dei clienti che lo hanno acquistato

    def __hash__(self):
        return hash(self.AlbumId)

    def __eq__(self, other):
        return isinstance(other, Album) and self.AlbumId == other.AlbumId

    def __str__(self):
        return self.Title