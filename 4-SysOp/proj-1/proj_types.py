# Tipos do problema
from time import sleep
from queue import Queue
from threading import Lock, Semaphore, Thread

MUTEX = Lock()
AGUARDAR_EMBARQUE = Semaphore(0)
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

  def __init__(self, vagas:int, t_viagem:int, status:int = 0) -> None:
    # Instanciando Thread
    Thread.__init__(self)

    # atributos do vagão
    self._STATUS_VAGAO = ['dormindo', 'percorrendo']
    self._executando = True
    self._vagas = vagas
    self._tempo_viagem = t_viagem

    self.status = self._STATUS_VAGAO[status]
    self.assentos:list[Passageiro] = []
    
    # Semáforos
    self.vagao_livre = Semaphore(0)
    self.pode_embarcar = Semaphore(0)
    self.pode_desembarcar = Semaphore(0)
    self.pode_passear = Semaphore(0)

  def esta_cheio(self) -> bool:
    with MUTEX:
      return True if len(self.assentos) == self._vagas else False
  
  def iniciar_passeio(self) -> None:
    with MUTEX:
      print('iniciando passeio')
      self.status = self._STATUS_VAGAO[1]

  def realizar_passeio(self) -> None:
    print('passeando')
    sleep(self._tempo_viagem)
    print('fim do passeio')
    with MUTEX:
      self.status = self._STATUS_VAGAO[0]

  def run(self):
    while True:
      self.pode_passear.acquire()

      self.iniciar_passeio()
      for i in range(self._vagas):
        AGUARDAR_EMBARQUE.release()
      
      self.realizar_passeio()
      for i in range(self._vagas):
        self.pode_desembarcar.release()
      
      self.vagao_livre.acquire()
      self.pode_embarcar.release()


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
