# Algoritmos de ordenação
import numpy as np
from time import perf_counter
from pandas import DataFrame
from seaborn import pointplot, set_style

# Constante
LISTA_DE_TAMANHOS = np.array([1000, 2000, 3000,
                              4000, 5000, 8000,
                              11_000, 15_000], dtype=int)

def testa_algoritmo(func:'function', tamanhos:'list[int]'=LISTA_DE_TAMANHOS) -> DataFrame:
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


# ALGORITMOS DE ORDENAÇÃO


def bubble(arr:np.ndarray) -> None:
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


def selection(arr:'np.ndarray[float]') -> None:
  """
  Selection Sort
  ---
  Ordena o arr de forma crescente.
  Dado o array de tamanho `n`, em cada iteração `i` define:
  `arr[i]` como o menor elemento dentro do pedaço `arr[i:n]`;
  o elemento que estava previamente em `arr[i]` troca de lugar
  com o novo
  """
  n = len(arr)
  i = 0
  for i in range(n):
    i_min = i
    for j in range(i, n):
      if arr[j] < arr[i]:
        i_min = j
    arr[i], arr[i_min] = arr[i_min], arr[i]


def insertion(arr:'np.ndarray[float]') -> None:
  """
  Insertion Sort
  ---
  Em cada iteração i, troca o elemento arr[i]
  de posição com o anterior caso este seja maior,
  esse processo acaba ao chegar no início do array
  ou o elemento anterior não ser maior que o da iteração.
  """
  n = len(arr)
  if n > 1:
    for i in range(1, n):
      atual = arr[i]
      j = i - 1
      while j >= 0 and arr[j] > atual:
        arr[j+1] = arr[j]
        j -= 1
      arr[j+1] = atual


def quick(arr:'np.ndarray[float]', start:int=0, stop:int=None) -> None:
  """
  Quick Sort
  ---
  Ordena o arr recursivamente de forma crescente.
  A cada chamada, define `pivo` como sendo o ultimo elemento do
  slice `arr[start, stop]` e agrupa no início dele os elementos que
  são menores que ele, depois repete o processo recursivamente para
  os slices menores e maiores do que o `pivo`.
  
  * OBS: definir limite de recursividade para algo pouco maior que
  `len(arr) ** 2` para não estourar a pilha de recursividade no pior
  caso:

  ```python
  from sys import setrecursionlimit
  setrecursionlimit(int(1.1 * len(arr)**2))
  ```
  """
  stop = stop if stop is not None else len(arr)
  i = start
  if i < stop:
    pivo = arr[stop-1]
    # agrupa os elementos menores que o pivô no início no array
    for j in range(start, stop):
      if arr[j] < pivo:
        arr[j], arr[i] = arr[i], arr[j]
        i += 1
  
    # posiciona o pivô na posição i separando os grupos de menores e maiores que ele
    arr[i], arr[stop-1] = arr[stop-1], arr[i]

    # repete o processo recursivamente
    quick(arr, start, i)
    quick(arr, i+1, stop)


def count(arr:'np.ndarray[int]'):
  """
  O algoritmo leva em consideração que os elementos do array são
  inteiros.
  """
  copia = arr.copy()
  minimo, maximo = arr.min(), arr.max()
  counts = np.zeros(maximo - minimo + 1, dtype=int)

  for element in arr:
    counts[element - minimo] += 1
  
  for i in range(1, len(counts)):
    counts[i] += counts[i-1]
  
  for e in copia:
    arr[counts[e - minimo] - 1] = e
    counts[e - minimo] -= 1


def bucket(arr:'np.ndarray[int]') -> None:
  """Bucket Sort"""
  LEN_BUCKET = 10

  bucket_min, bucket_max = min(arr), max(arr)

  n_buckets = (bucket_max - bucket_min) // LEN_BUCKET + 1
  
  buckets_list = [[] for _ in range(n_buckets)]

  # Colocando elementos nos baldes
  for e in arr:
    pos = (e - bucket_min) // LEN_BUCKET
    buckets_list[pos].append(e)
  
  # Ordenando baldes
  pos = 0
  for balde in buckets_list:
    balde = sorted(balde)
    for num in balde:
      arr[pos] = num
      pos += 1



if __name__ == '__main__':
  a = np.array([8, 5, 12, 55, 3, 7, 82, 44, 35, 25, 41, 29, 17])
  pass
