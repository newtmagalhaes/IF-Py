# Tipos de Fila e Páginas usados
from dataclasses import dataclass

@dataclass
class Pagina:
  id:str
  R:bool
  M:bool

@dataclass
class _Node:
  pagina:Pagina
  next: '_Node|None' = None

class Fila:
  def __init__(self, limite:int) -> None:
    self.limite = limite
    self.capacidade = 0
    self.head : '_Node|None' = None
  
  def __str__(self) -> str:
    s = '['
    node = self.head
    while node is not None:
      s += f'{node.pagina.id} - '
      node = node.next
    return s + ']'

  def esta_vazia(self) -> bool:
    return self.capacidade == 0
  
  def esta_cheia(self) -> bool:
    return self.capacidade == self.limite
  
  def encontrar(self, id:str) -> bool:
    i = 0
    node = self.head
    while node is not None:
      if node.pagina.id == id:
        return i
      i += 1
      node = node.next
    return -1

  def enfilar(self, pag:Pagina) -> None:
    if self.head is None:
      self.head = _Node(pag)
    else:
      node = self.head
      while node.next is not None:
        node = node.next
      node.next = _Node(pag)
    self.capacidade += 1
    

  def desenfilar(self) -> Pagina:
    out = self.head
    if out is not None:
      self.head = self.head.next
      out.next = None
    self.capacidade -= 1
    return out
