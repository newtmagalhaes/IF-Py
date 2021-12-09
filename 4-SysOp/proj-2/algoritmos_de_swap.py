# Implementação de algoritmos de swap
from fila_e_pagina import Fila, Pagina

# Algoritmos de Swap
def fifo(limite:int, ref_list:'list[str]', delta_t:int=0) -> int:
  '''FIFO (First-In First-Out)'''
  f = Fila(limite)
  acerto = 0
  for ref in ref_list:
    id = ref[:-1]
    if f.encontrar(id) >= 0:
      acerto += 1
    else:
      if f.esta_cheia():
        f.desenfilar()
      f.enfilar(Pagina(id))
  return acerto


def mru(limite:int, ref_list:'list[str]', delta_t:int=0) -> int:
  '''Menos recentemente Usada'''
  f = Fila(limite)
  acerto = 0
  for ref in ref_list:
    id = ref[:-1]
    pos = f.encontrar(id)
    if pos >= 0:
      acerto += 1
      aux = f.desenfilar(pos)
      f.enfilar(aux)
    else:
      if f.esta_cheia():
        f.desenfilar()
      f.enfilar(Pagina(id))
  return acerto


def sc(limite:int, ref_list:'list[str]', delta_t:int=30) -> int:
  '''Segunda Chance'''
  f = Fila(limite)
  acerto = 0
  for i, ref in enumerate(ref_list):
    # Se i for multiplo de delta_t
    if i % delta_t == 0:
      for pag in f.pag_list:
        pag.bit_R = 0 # Reseta o bit R das páginas na fila

    id = ref[:-1]
    pos = f.encontrar(id)
    if pos >= 0:
      f.pag_list[pos].bit_R = 1
      acerto += 1
    else:
      if f.esta_cheia():
        # Enquanto o bit R da primeira página for 1
        while f.pag_list[0].bit_R:
          aux = f.desenfilar()
          aux.bit_R = 0
          f.enfilar(aux)
        f.desenfilar()
      f.enfilar(Pagina(id, 1))
  return acerto


def nur(limite:int, ref_list:'list[str]', delta_t:int=30) -> int:
  '''Não Usada Recentemente'''
  f = Fila(limite)
  acerto = 0
  for i, ref in enumerate(ref_list):
    # Se i for multiplo de delta_t
    if i % delta_t == 0:
      for pag in f.pag_list:
        pag.bit_R = 0

    id = ref[:-1]
    ultimo_caracter = ref[-1] # Sempre 'R' (leitura) ou 'W' (escrita)
    pos = f.encontrar(id)
    if pos >= 0:
      f.pag_list[pos].bit_R = 1
      acerto += 1
      if ultimo_caracter == 'W':
        f.pag_list[pos].bit_M = 1

    else:
      if f.esta_cheia():
        # como classe varia de 0 a 3, qualquer valor
        # entrará na condição pelo menos uma vez
        menor_classe = 4
        pos_menor_classe = 0
        for pos, pag in enumerate(f.pag_list):
          classe_da_pag = 2*pag.bit_R + 1*pag.bit_M
          if classe_da_pag < menor_classe:
            menor_classe = classe_da_pag
            pos_menor_classe = pos
        f.desenfilar(pos_menor_classe)
      modo = 1 if ultimo_caracter == 'W' else 0
      f.enfilar(Pagina(id, bit_R=1, bit_M=modo))

  return acerto


ALGORITMOS = [fifo, mru, sc, nur]

if __name__ == '__main__':
  print('teste 1')
  DELTA_T = 30
  ENTRADA = '5W-5R-2R-7R-8R-'
  REFERENCIAS = ENTRADA.split('-')[:-1] # este slice exclui o ultimo elemento (que seria '')

  # # Pegando input do arquivo.txt
  with open('4-SysOp/proj-2/REFERENCIAS_1000.TXT') as file:
    txt = file.read().split('-')[:-1]
    for algoritmo in ALGORITMOS:
      for n_frames in [2]:
        acertos = algoritmo(n_frames, txt, DELTA_T)
        print(f'{algoritmo.__name__} com {n_frames} frames: {acertos} acertos')
