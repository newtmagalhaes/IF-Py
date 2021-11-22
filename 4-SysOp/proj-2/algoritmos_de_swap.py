# Implementação de algoritmos de swap
import numpy as np
import pandas as pd
from fila_e_pagina import Fila, Pagina


# Algoritmos de Swap
def fifo(queue:Fila, ref_list:'list[str]') -> int:
  acerto = 0
  for ref in ref_list:
    id = ref[:-1]
    if queue.encontrar(id) >= 0:
      acerto += 1
    else:
      if queue.esta_cheia():
        queue.desenfilar()
      queue.enfilar(Pagina(id, 1, 0))
  print(queue)
  return acerto



def sc():
  pass


def mru():
  pass


def nur():
  pass

if __name__ == '__main__':
  # # Pegando input do arquivo.txt
  # with open('4-SysOp/proj-2/REFERENCIAS_1000.TXT') as file:
  #   txt = file.read().split('-')[:-1]
  #   print(len(txt))

  TESTE = '2W-1R-5R-5W-2R-0W-2R-7R-1W-7W-2R-7W-4R-2R-6W-1W-2W-3W-7R-5R-'
  REFERENCIAS = TESTE.split('-')[:-1] # este slice exclui o ultimo elemento (que seria '')
  # FRAMES = (3, 4) # (50, 70, 90)

  acertos = fifo(Fila(4), REFERENCIAS)
  print(f'acertos: {acertos}')
  # acertos = {}
  # for alg in [fifo]:
  #   acertos[alg.__name__] = []
  #   for n_frames in FRAMES:
  #     acertos = alg(REFERENCIAS)
  #     acertos[alg.__name__].append(acertos)
  
    
