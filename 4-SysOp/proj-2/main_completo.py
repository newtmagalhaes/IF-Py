#%% Tipos de Fila e Páginas usados no projeto
from dataclasses import dataclass

@dataclass
class Pagina:
  id:str
  bit_R:int = 0
  bit_M:int = 0
  classe:int = 0

class Fila:
  def __init__(self, limite:int) -> None:
    '''Imita o comportamento de uma Fila de Páginas'''
    self.LIMITE = limite
    self.frames_ocupados = 0
    self.pag_list:'list[Pagina]' = []
  
  def __str__(self) -> str:
    s = '['
    for pag in self.pag_list:
      s += f' {pag.id} -'
    return s[:-1] + ']'

  def esta_vazia(self) -> bool:
    return self.frames_ocupados == 0
  
  def esta_cheia(self) -> bool:
    return self.frames_ocupados == self.LIMITE
  
  def encontrar(self, id:str) -> int:
    '''
    Verifica se a fila possui uma página com o `id` especificado.
    - Se tiver: retorna a posição da página na fila;
    - Senão: retorna -1; 
    '''
    for i, pag in enumerate(self.pag_list):
      if pag.id == id:
        return i
    return -1


  def enfilar(self, pag:Pagina) -> None:
    '''
    Adiciona a página no fim da fila se a mesma
    não estiver cheia.
    '''
    if not self.esta_cheia():
      self.pag_list.append(pag)
      self.frames_ocupados += 1
    

  def desenfilar(self, pos : int = 0) -> 'Pagina|None':
    '''
    Remove o elemento da posição `pos` da fila e o retorna;
    Retorna `None` se a fila estiver vazia;
    Gera erro se o indice `pos` exceder o tamanho da fila.
    '''
    if not self.esta_vazia():
      out = self.pag_list.pop(pos)
      self.frames_ocupados -= 1
      return out


#%% Implementando Algoritmos de substituição de páginas
def fifo(limite:int, ref_list:'list[str]', delta_t:int=0) -> int:
  '''
  # FIFO (First-In First-Out)
  Mantém uma lista encadeada de todas as páginas:
  - A página mais antiga está cabeça da fila;
  - A página que chegou por último na memória é colocada no final da fila;
  - Na ocorrência de falta de página:
    - A página na cabeça da fila é removida;
    - A nova página é adicionada no final da fila;
  - Desvantagem
    - Páginas muito usadas podem ser removidas.
'''
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
  ''''''
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


def sc(limite:int, ref_list:'list[str]', delta_t:int=50) -> int:
  '''
  # Segunda Chance
  Modificação do FIFO para evitar que páginas muito usadas sejam removidas da memória.
  - Faz-se uso do `bit_R` (indica se a página foi referenciada):
  - Quando uma página é referenciada, seu `bit_R` é setado (= True);
  - A cada `delta_t` iterações, o algoritmo zera o `bit_R` de todas as páginas na fila;
  - Na ocorrência de falta de página:
    - Examina o `bit_R` da página mais antiga (cabeça da fila):
      - `bit_R` = False => A página não está sendo usada e será substituída;
      - `bit_R` = True  => O algoritmo zera o `bit_R` e coloca a página no final da fila;
'''
  f = Fila(limite)
  acerto = 0
  for i, ref in enumerate(ref_list):
    id = ref[:-1]
    if i % delta_t == 0:
      # Se i for multiplo de delta_t
      for pag in f.pag_list:
        pag.bit_R = 0
    pos = f.encontrar(id)
    if pos >= 0:
      f.pag_list[pos].bit_R = 1
      acerto += 1
    else:
      if f.esta_cheia():
        while f.pag_list[0].bit_R:
          aux = f.desenfilar()
          aux.bit_R = 0
          f.enfilar(aux)
        f.desenfilar()
      f.enfilar(Pagina(id, 1))
  return acerto


def nur(limite: int, ref_list: 'list[str]', delta_t: int = 0) -> int:
  ''''''
  f = Fila(limite)
  acerto = 0
  for i, ref in enumerate(ref_list):
    id = ref[:-1]
    ultimo_caracter = ref[-1]
    if i % delta_t == 0:
      # Se i for multiplo de delta_t
      for pag in f.pag_list:
        pag.bit_R = 0
        if pag.bit_M == 0:
          pag.classe = 0
        else:
          pag.classe = 1

    pos = f.encontrar(id)
    if pos >= 0:
      f.pag_list[pos].bit_R = 1
      acerto += 1
      if ultimo_caracter == 'W':
        f.pag_list[pos].bit_M = 1
        f.pag_list[pos].classe = 3
    else:
      if f.esta_cheia():
        # como classe varia de 0 a 3, qualquer valor
        # entrará na condição pelo menos uma vez
        menor_classe = 4
        pos_menor_classe = 0
        for pos, pag in enumerate(f.pag_list):
          if pag.classe < menor_classe:
            menor_classe = pag.classe
            pos_menor_classe = pos
        f.desenfilar(pos_menor_classe)
      if ultimo_caracter == 'W':
        f.enfilar(Pagina(id, 1, 1, 3)) 
      else:
        f.enfilar(Pagina(id, 1, 0, 2))

  return acerto

#%% Implementando interface
# imports usados no arquivo
from tkinter import (Tk, StringVar, ttk, filedialog)
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from seaborn import pointplot, set_style
set_style(style='darkgrid')

class App(Tk):
  def __init__(self):
    super().__init__()
    # Set janela
    self.wm_title('Projeto 2')
    self.configure(background='white')

    # Set busca de arquivo
    self.app_txt_path = StringVar(value='Nenhum arquivo definido')
    ttk.Label(self, textvariable=self.app_txt_path)\
      .grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    ttk.Button(self, text='Escolher arquivo txt', command=self.app_escolher_arquivo)\
      .grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    
    # Set entrada de número de Frames
    self.app_frame_min = StringVar(value='0')
    self.app_frame_max = StringVar(value='1')
    ttk.Label(self, text='Defina os intervalos de Frames')\
      .grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Label(self, text='De:').grid(row=3, column=0)
    ttk.Entry(self, textvariable=self.app_frame_min, width=3)\
      .grid(row=3, column=1)
    ttk.Label(self, text='até:').grid(row=4, column=0)
    ttk.Entry(self, textvariable=self.app_frame_max, width=3)\
      .grid(row=4, column=1)

    # Set delta T
    self.app_delta_t = StringVar(value=30)
    ttk.Label(self, text='Defina delta T:')\
      .grid(row=5, column=0, padx=5, pady=5)
    ttk.Entry(self, textvariable=self.app_delta_t, width=3)\
      .grid(row=5, column=1, padx=5, pady=5)

    # Executar algoritmos
    ttk.Button(self, text='Executar algoritmos', command=self.app_executar)\
      .grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    self.app_fig, self.app_ax = plt.subplots(figsize=(6, 4))
    self.app_canvas = FigureCanvasTkAgg(figure=self.app_fig, master=self)
    self.app_canvas.get_tk_widget().grid(row=0, rowspan=6, column=2)
    self.app_tabela = StringVar()

    ttk.Label(self, textvariable=self.app_tabela)\
      .grid(row=0, rowspan=6, column=3, padx=5, pady=5)
  
  def app_escolher_arquivo(self):
    txt_path = filedialog.askopenfilename(defaultextension='txt')
    self.app_txt_path.set(txt_path)
  
  def app_executar(self):
    # Se a string tem a extensão txt
    if '.txt' in self.app_txt_path.get().lower():
      frame_range = range(int(self.app_frame_min.get()), int(self.app_frame_max.get()) + 1, 20)
      ALGORITMOS = [fifo, sc, mru, nur]
      resultados = {func.__name__.upper():[] for func in ALGORITMOS}
      resultados['FRAMES'] = frame_range

      # Pegando input do arquivo.txt
      with open(self.app_txt_path.get()) as file:
        txt = file.read().split('-')[:-1]
        for func in ALGORITMOS:
          for n_frames in frame_range:
            n_acerto = func(n_frames, txt, int(self.app_delta_t.get()))
            resultados[func.__name__.upper()].append(n_acerto)
      
      df = DataFrame(resultados)
      self.app_tabela.set(df)
      long_df = df.melt('FRAMES', var_name='algoritmos', value_name='acertos')

      # Atualizando imagem do GUI
      self.app_ax.clear()
      pointplot(data=long_df,
                x='FRAMES',
                y='acertos',
                hue='algoritmos',
                ax=self.app_ax
                ).set(title='Algoritmos de substituição de páginas',
                      xlabel='Quantidade de Frames',
                      ylabel='Quantidade de Acertos')
      self.app_canvas.draw()
      # ax.get_figure().savefig('output.png')
    # Para teste apenas
    else:
      data = {'FRAMES':[50, 70, 90],
              'FIFO':[480, 662, 833],
              'SC':  [488, 666, 837],
              'MRU': [478, 657, 824],
              'NUR': [484, 671, 839]}
      df = DataFrame(data)
      self.app_tabela.set(df)
      long_df = df.melt('FRAMES', var_name='algoritmos', value_name='acertos')
      # print(long_df)

      self.app_ax.clear()
      pointplot(data=long_df,
                x='FRAMES',
                y='acertos',
                hue='algoritmos',
                ax=self.app_ax
                ).set(title='Algoritmos de substituição de páginas',
                      xlabel='Quantidade de Frames',
                      ylabel='Quantidade de Acertos')
      # ax.get_figure().savefig('output.png')
      self.app_canvas.draw()
      
      

#%% Main
if __name__ == '__main__':
  App().mainloop()
