# Tipos do problema
from time import sleep
from threading import Lock, Semaphore, Thread
from typing import Callable, List
from tkinter import StringVar


class Vagao(Thread):
  def __init__(self,
               vagas:int,
               t_viagem:int,
               log_text:StringVar,
               log_hist:List[str],
               log_func:Callable[[str, StringVar, List[str]], None]) -> None:
    """
    Uma thread que representa um vagão de montanha russa.

    Parâmetros
    ---
    - vagas: deve ser >= 0. Quantidade de passageiros que o vagão suporta;
    - t_viagem: deve ser >= 0. Tempo (em segundos) que o vagão leva para
    completar um passeio;
    """
    # Instanciando Thread
    Thread.__init__(self)

    # atributos do vagão
    self._STATUS_VAGAO = ['dormindo', 'percorrendo']
    self._executando = True
    self._vagas = vagas
    self._tempo_viagem = t_viagem
    self._log_text = log_text
    self._log_hist = log_hist
    self._log_func = log_func

    self.status = self._STATUS_VAGAO[0]
    self.assentos:list[Passageiro] = []
    
    # Semáforos
    self.MUTEX = Lock()
    self.AGUARDAR_EMBARQUE = Semaphore(0)
    self.vagao_livre = Semaphore(0)
    self.pode_embarcar = Semaphore(1)
    self.pode_desembarcar = Semaphore(0)
    self.pode_passear = Semaphore(0)

  def desligar(self) -> None:
    self._log_func('Fim do expediente', self._log_text, self._log_hist)
    self._executando = False

  def esta_vago(self):
    return True if len(self.assentos) == 0 else False

  def esta_cheio(self) -> bool:
    return True if len(self.assentos) == self._vagas else False
  
  def iniciar_passeio(self) -> None:
    with self.MUTEX:
      self._log_func('iniciando passeio', self._log_text, self._log_hist)
      self.status = self._STATUS_VAGAO[1]

  def realizar_passeio(self) -> None:
    self._log_func('passeando', self._log_text, self._log_hist)
    sleep(self._tempo_viagem)
    self._log_func('fim do passeio', self._log_text, self._log_hist)
    with self.MUTEX:
      self.status = self._STATUS_VAGAO[0]

  def run(self):
    while self._executando:
      self.pode_passear.acquire()

      self.iniciar_passeio()
      for _ in range(self._vagas):
        self.AGUARDAR_EMBARQUE.release()
      
      self.realizar_passeio()
      for _ in range(self._vagas):
        self.pode_desembarcar.release()
      
      self.vagao_livre.acquire()
      self.pode_embarcar.release()
    
    self._log_func('Vagão voltando para garagem', self._log_text, self._log_hist)
    sleep(5)


class Passageiro(Thread):
  """
  Uma thread representando os passageiros do problema.

  Parâmetros
  ---
  * id:str;
  * t_embarque:int;
  * t_desembarque:int;
  * vagao: Vagao
  * fila: list[Passageiro]
  * status
  """
  
  def __init__(self,
               id:str,
               t_embarque:int,
               t_desembarque:int,
               vagao:Vagao,
               fila:list,
               log_text:StringVar,
               log_hist:List[str],
               log_func:Callable[[str, StringVar, List[str]], None]) -> None:
    # Instanciando thread
    Thread.__init__(self)

    # Atributos do passageiro
    self._STATUS_PASSAGEIROS = ['dormindo', 'apreciando',
                                'embarcando', 'desembarcando']
    self._vagao = vagao
    self._fila:list[Passageiro] = fila
    self._log_text = log_text
    self._log_hist = log_hist
    self._log_func = log_func


    self.status = self._STATUS_PASSAGEIROS[0]
    self.id = id
    self.t_embarque = t_embarque
    self.t_desembarque = t_desembarque

  def sair_da_fila(self) -> None:
    self._log_func(f'Passageiro {self.id} saindo da fila', self._log_text, self._log_hist)
    for i, passageiro in enumerate(self._fila):
      if passageiro is self:
        self._fila.pop(i)

  def entrar_na_fila(self) -> None:
    self._log_func(f'Passageiro {self.id} entrou na fila', self._log_text, self._log_hist)
    self.status = self._STATUS_PASSAGEIROS[0]
    self._fila.append(self)

  def embarcar(self) -> None:
    self._log_func(f'Passageiro {self.id} embarcando', self._log_text, self._log_hist)
    self.status = self._STATUS_PASSAGEIROS[2]
    self._vagao.assentos.append(self)
    sleep(self.t_embarque)

  def desembarcar(self) -> None:
    self._log_func(f'Passageiro {self.id} desembarcando', self._log_text, self._log_hist)
    self.status = self._STATUS_PASSAGEIROS[3]
    for i, passageiro in enumerate(self._vagao.assentos):
      if passageiro is self:
        self._vagao.assentos.pop(i)
    sleep(self.t_desembarque)

  def apreciar_paisagem(self) -> None:
    self._log_func(f'Passageiro {self.id} apreciando paisagem', self._log_text, self._log_hist)
    self.status = self._STATUS_PASSAGEIROS[1]
    sleep(2)
  
  def run(self):
    with self._vagao.MUTEX:
      self.entrar_na_fila()
    
    while self._vagao._executando:
      if self == self._fila[0]:
        self._vagao.pode_embarcar.acquire()
        # Se o vagão não estiver mais executando após o release
        if not self._vagao._executando:
          break

        with self._vagao.MUTEX:
          self.sair_da_fila()
          self.embarcar()
          if self._vagao.esta_cheio():
            self._vagao.pode_passear.release()
          else:
            self._vagao.pode_embarcar.release()

        self._log_func(f'Passageiro {self.id} aguardando embarque', self._log_text, self._log_hist)
        self._vagao.AGUARDAR_EMBARQUE.acquire()
        while self._vagao.status == 'percorrendo':
          self.apreciar_paisagem()
        self._vagao.pode_desembarcar.acquire()
        with self._vagao.MUTEX:
          self.desembarcar()
          self.entrar_na_fila()
          if self._vagao.esta_vago():
            self._vagao.vagao_livre.release()
      else:
        sleep(2)
    
    with self._vagao.MUTEX:
      self.sair_da_fila()
      self._log_func(f'Passageiro {self.id} indo embora', self._log_text, self._log_hist)

# Bloco para testes
if __name__ == '__main__':
  from typing import List

  # Constantes
  N_PASSAGEIROS = 4
  N_VAGAS = 2
  T_VIAGEM = 3

  # Alocando Objetos
  print('Iniciando aplicação')
  v = Vagao(N_VAGAS, T_VIAGEM)
  v.start()

  f : List[Passageiro] = []
  for i in range(N_PASSAGEIROS):
    p = Passageiro(f'{i}', 2, 2, v, f)
    p.start()
  
  sleep(10)
  v.desligar()
  v.join()
  for passageiro in f:
    p.join()
  
  print('tudo ok!')
