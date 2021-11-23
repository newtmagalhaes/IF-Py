# Tipos de Fila e Páginas usados no projeto
from dataclasses import dataclass

@dataclass
class Pagina:
  id:str
  R:bool = 0
  M:bool = 0

class Fila:
  def __init__(self, limite:int) -> None:
    '''
    Imita o comportamento de uma Fila de Páginas
    '''
    self.LIMITE = limite
    self.frames_ocupados = 0
    self.pag_list:'list[Pagina]' = []
  
  def __str__(self) -> str:
    s = '['
    for pag in self.pag_list:
      s += f' {pag.id} -'
    return s[:-1] + ']'

  def esta_vazia(self) -> bool:
    return self.frames_ocupados == 0
  
  def esta_cheia(self) -> bool:
    return self.frames_ocupados == self.LIMITE
  
  def encontrar(self, id:str) -> int:
    '''
    Verifica se a fila possui uma página com o `id` especificado.
    - Se tiver: retorna a posição da página na fila;
    - Senão: retorna -1; 
    '''
    for i, pag in enumerate(self.pag_list):
      if pag.id == id:
        return i
    return -1

  def enfilar(self, pag:Pagina) -> None:
    '''
    Adiciona a página no fim da fila se a mesma
    não estiver cheia.
    '''
    if not self.esta_cheia():
      self.pag_list.append(pag)
      self.frames_ocupados += 1
    

  def desenfilar(self, pos : int = 0) -> 'Pagina|None':
    '''
    Remove o elemento da posição `pos` da fila e o retorna;
    
    Retorna `None` se a fila estiver vazia;
    
    Gera erro se o indice `pos` exceder o tamanho da fila.
    '''
    if not self.esta_vazia():
      out = self.pag_list.pop(pos)
      self.frames_ocupados -= 1
      return out
