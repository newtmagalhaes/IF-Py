# Implementação de algoritmos de swap
from fila_e_pagina import Fila, Pagina

# Algoritmos de Swap
def fifo(f:Fila, ref_list:'list[str]') -> int:
  acerto = 0
  for ref in ref_list:
    id = ref[:-1]
    if f.encontrar(id) >= 0:
      acerto += 1
    else:
      if f.esta_cheia():
        f.desenfilar()
      f.enfilar(Pagina(id, 1, 0))
  return acerto


def mru(f:Fila, ref_list:'list[str]') -> int:
  pass


# Usado nos algoritmos Segunda Chance e NUR
DELTA_T = 50


def sc(f:Fila, ref_list:'list[str]') -> int:
  pass


def nur(f:Fila, ref_list:'list[str]') -> int:
  pass


if __name__ == '__main__':
  print('teste 1')
  ENTRADA = '2W-1R-5R-5W-2R-0W-2R-7R-1W-7W-2R-7W-4R-2R-6W-1W-2W-3W-7R-5R-'
  REFERENCIAS = ENTRADA.split('-')[:-1] # este slice exclui o ultimo elemento (que seria '')
  f = Fila(4)
  acertos = fifo(f, REFERENCIAS)
  # Fila no final com FIFO é: [1, 3, 7, 5] - 8 acertos
  print(f'Fila no final da execução: {f}\nacertos: {acertos}')

  print('teste 2')
  # # Pegando input do arquivo.txt
  with open('4-SysOp/proj-2/REFERENCIAS_1000.TXT') as file:
    txt = file.read().split('-')[:-1]
    for n_frames in [50, 70, 90]:
      for algoritmo in [fifo]:
        acertos = algoritmo(Fila(n_frames), txt)
        print(f'{algoritmo.__name__} com {n_frames} frames: {acertos} acertos')
