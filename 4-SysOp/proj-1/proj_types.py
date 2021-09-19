from threading import Lock, Semaphore, Thread


class Vagao(Thread):
  """
  Uma thread que representa um vagão de montanha russa.

  Parâmetros
  ---
  * vagas: deve ser >= 0. Quantidade de passageiros que o vagão suporta;
  * t_viagem: deve ser >= 0. Tempo (em segundos) que o vagão leva para
  completar um passeio;
  """

  def __init__(self, vagas:int, t_viagem:int):
    Thread.__init__(self)
    self.t_viagem = t_viagem
    self.vagas = vagas
  
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
  
  def __init__(self, id:str, t_embarque:int, t_desembarque:int):
    Thread.__init__(self)
    self.t_desembarque = t_desembarque
    self.t_embarque = t_embarque
    self.id = id
  
  def run(self):
    pass
