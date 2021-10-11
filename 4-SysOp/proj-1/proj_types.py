# Tipos do problema
from time import sleep
from threading import Lock, Semaphore, Thread

MUTEX = Lock()
AGUARDAR_EMBARQUE = Semaphore(0)

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
  
  def __init__(self,
               id:str,
               t_embarque:int,
               t_desembarque:int,
               vagao:Vagao,
               fila:list,
               status : int = 0) -> None:
    # Instanciando thread
    Thread.__init__(self)

    # Atributos do passageiro
    self._STATUS_PASSAGEIROS = ['dormindo', 'apreciando',
                                'embarcando', 'desembarcando']
    self._vagao = vagao
    self._fila = fila

    self.status = self._STATUS_PASSAGEIROS[status]
    self.id = id
    self.t_embarque = t_embarque
    self.t_desembarque = t_desembarque

  def entrar_na_fila(self) -> None:
    print(f'Passageiro {self.id} entrou na fila')
    self._fila.append(self)

  def embarcar(self) -> None:
    print(f'Passageiro {self.id} embarcando')
    self._vagao.assentos.append(self)
    sleep(self.t_embarque)

  def desembarcar(self) -> None:
    print(f'Passageiro {self.id} desembarcando')
    for i, passageiro in enumerate(self._vagao.assentos):
      if passageiro is self:
        self._vagao.assentos.pop(i)
    sleep(self.t_desembarque)

  def apreciar_paisagem(self) -> None:
    print(f'Passageiro {self.id} apreciando paisagem')
    sleep(2)
  
  def run(self):
    self.entrar_na_fila()
    while True:
      if self is self._fila[0]:
        self._vagao.pode_embarcar.acquire()
        with MUTEX:
          self.embarcar()
          if self._vagao.esta_cheio():
            self._vagao.pode_passear.release()
          else:
            self._vagao.pode_embarcar.release()
        
        AGUARDAR_EMBARQUE.acquire()
        while self._vagao.status == 'percorrendo':
          self.apreciar_paisagem()
        self._vagao.pode_desembarcar.acquire()
        with MUTEX:
          self.desembarcar()
          self.entrar_na_fila()
          if self._vagao.esta_vago():
            self._vagao.vagao_livre.release()
      else:
        sleep(2)

# Bloco para testes
if __name__ == '__main__':
  pass
