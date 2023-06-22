from dataclasses import dataclass
from typing import Any


@dataclass
class _DeletedPosition:
    def __getitem__(self, item) -> False:
        return None

    def __bool__(self):
        return False


# Enderecamento Aberto
class TabelaHash:
    def __init__(self, size: int = 1000):
        self.SIZE = size
        self.tabela: 'list[None|tuple[Any, Any]]' = [None] * size

    def _hash(self, chave) -> int:
        return hash(chave) % self.SIZE

    def insert(self, chave, valor):
            pos = self._hash(chave)

            for i in range(1, self.SIZE):
                if isinstance(self.tabela[pos], (_DeletedPosition, type(None))):
                    self.tabela[pos] = (chave, valor)
                    return
                pos = (pos + i) % self.SIZE

            raise ValueError('Tabela cheia')

    def search(self, chave):
        pos = self._hash(chave)

        for i in range(1, self.SIZE):
            if self.tabela[pos] is None:
                return
            elif self.tabela[pos][0] == chave:
                return self.tabela[pos][1]
            pos = (pos + i) % self.SIZE


    def delete(self, chave):
        pos = self._hash(chave)

        for i in range(1, self.SIZE):
            if self.tabela[pos] is None:
                return
            elif self.tabela[pos][0] == chave:
                self.tabela[pos] = _DeletedPosition()
                print(f"par {self.tabela[pos]} deletado")
                return
            pos = (pos + i) % self.SIZE

# %%
from typing_extensions import Self
from dataclasses import dataclass
from typing import Any


@dataclass
class _Node:
    key: Any
    value: Any
    next: 'Self|None' = None

    def __repr__(self) -> str:
        return ('{' f'{self.key}:{self.value}' '}')

# Encadeamento Separado
class HashTable:
    def __init__(self, size: int = 1000):
        self.SIZE = size
        self.tabela: 'list[_Node|None]' = [None] * size

    def __setitem__(self, key, value):
        self.insert(key, value)
    
    def __getitem__(self, key):
        return self.search(key)

    def _hash(self, chave) -> int:
        return hash(chave) % self.SIZE

    def insert(self, chave, valor):
            pos = self._hash(chave)
            if self.tabela[pos] is None:
                self.tabela[pos] = _Node(chave, valor)
            else:
                current = self.tabela[pos]
                while current.next:
                    current = current.next
                print("Inserido com colisão")
                current.next = _Node(chave, valor)

    def search(self, chave):
        pos = self._hash(chave)

        if current := self.tabela[pos]:
            while current.key != chave:
                if current.next is None:
                    return
                current = current.next
            return current.value

    def delete(self, chave):
        pos = self._hash(chave)

        if current := self.tabela[pos]:
            if current.key == chave:
                self.tabela[pos] = None
            else:
                while current.next:
                    if current.next.key == chave:
                        print(f"Nó {current.next} deletado")
                        current.next = current.next.next
                        return
                    current = current.next
