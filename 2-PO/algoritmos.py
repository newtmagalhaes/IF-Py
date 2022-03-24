# Algoritmos de ordenação
import numpy as np
from time import perf_counter
from pandas import DataFrame
from seaborn import pointplot, set_style

# Constante
LISTA_DE_TAMANHOS = np.array([1000, 2000, 3000,
                              4000, 5000, 8000,
                              11_000, 15_000], dtype=int)

def bubble_sort(arr:np.ndarray) -> None:
  i = 0
  n = len(arr)
  houve_troca = True
  while i < n-1 and houve_troca:
    i += 1
    houve_troca = False
    for j in range(n-1):
      if arr[j] > arr[j+1]:
        arr[j], arr[j+1] = arr[j+1], arr[j]
        houve_troca = True


def testa_algoritmo(func:function, tamanhos:'list[int]'=LISTA_DE_TAMANHOS) -> DataFrame:
  ''''''
  data = dict()
  for ordem in ['crescente', 'aleatoria', 'decrescente']:
    tempos = list()
    for tamanho in tamanhos:
      # Gerando amostra do teste
      if ordem == 'crescente':
        amostra = np.arange(tamanho, dtype=float)
      elif ordem == 'decrescente':
        amostra = np.arange(tamanho, dtype=float)[::-1].copy()
      else:
        amostra = np.random.sample(tamanho)
      
      # testando performance
      start = perf_counter()
      func(amostra)
      stop = perf_counter()
      
      # salvando resultado
      tempos.append(stop - start)
    data[ordem] = tempos
  data['tamanhos'] = LISTA_DE_TAMANHOS
  return DataFrame(data=data)

def gerar_plot(df:DataFrame) -> DataFrame:
  ''''''
  long_df = df.melt(id_vars='tamanhos',
                    var_name='ordenação',
                    value_name='tempos')
  
  set_style('darkgrid')
  pointplot(
    data=long_df,
    x='tamanhos',
    y='tempos',
    hue='ordenação',
    ).set(
      xlabel='tamanho da amostra',
      ylabel='tempo (s)',
      title='TAMANHO DA LISTA X TEMPO DE ORDENAMENTO')

  # Ordena a partir do maior tempo e pega o primeiro elemento da
  # coluna 'ordenação'
  ordem = long_df.sort_values(by='tempos', ascending=False)['ordenação'].values[0]
  print(f'O pior caso é quando a lista se encontra ordenada de forma {ordem}')
  return long_df

if __name__ == '__main__':
  pass