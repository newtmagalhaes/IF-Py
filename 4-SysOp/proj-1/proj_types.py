# Tipos do problema

from queue import Queue
from threading import Lock, Semaphore, Thread

MUTEX = Lock()
_STATUS_VAGAO = ['dormindo', 'percorrendo']
_STATUS_PASSAGEIROS = ['dormindo', 'apreciando',
                       'embarcando', 'desembarcando']

class Vagao(Thread):
  """
  Uma thread que representa um vagão de montanha russa.

  Parâmetros
  ---
  * vagas: deve ser >= 0. Quantidade de passageiros que o vagão suporta;
  * t_viagem: deve ser >= 0. Tempo (em segundos) que o vagão leva para
  completar um passeio;
  """

  def __init__(self, vagas:int, t_viagem:int) -> None:
    # Instanciando Thread
    Thread.__init__(self)

    # atributos do vagão
    self.vagas = vagas
    self.tempo_viagem = t_viagem
    self.assentos:list[Passageiro] = []
    
    # Semáforos
    self.pode_embarcar = Semaphore(0)
    self.pode_desembarcar = Semaphore(0)
    self.pode_passear = Semaphore(0)

  def esta_cheio(self) -> bool:
    pass
  
  def iniciar_passeio(self) -> None:
    pass

  def realizar_passeio(self) -> None:
    pass

  def run(self):
    pass


class Passageiro(Thread):
  """
  Uma thread representando os passageiros do problema.

  Parâmetros
  ---
  * id:str;
  * t_embarque:int;
  * t_desembarque:int;
  """
  
  def __init__(self, id:str, status:str, t_embarque:int, t_desembarque:int) -> None:
    # Instanciando thread
    Thread.__init__(self)

    # Atributos do passageiro
    self.id = id
    self.status = status
    self.t_embarque = t_embarque
    self.t_desembarque = t_desembarque

  def entrar_na_fila(self, fila:Queue) -> None:
    pass

  def embarcar(self, carrinho:Vagao) -> None:
    pass

  def desembarcar(self) -> None:
    pass

  def apreciar_paisagem(self) -> None:
    pass
  
  def run(self):
    pass

# Bloco para testes
if __name__ == '__main__':
  pass
