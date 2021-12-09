from algoritmos_de_swap import ALGORITMOS

from pandas import DataFrame
from tkinter import Tk, StringVar, ttk, filedialog
from tkinter.messagebox import showwarning
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
    self.app_frame_min = StringVar(value='50')
    self.app_frame_max = StringVar(value='90')
    self.app_frame_step = StringVar(value='20')
    ttk.Label(self, text='Defina os intervalos de Frames')\
      .grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Label(self, text='De:').grid(row=3, column=0)
    ttk.Entry(self, textvariable=self.app_frame_min, width=3)\
      .grid(row=3, column=1)
    ttk.Label(self, text='Até:').grid(row=4, column=0)
    ttk.Entry(self, textvariable=self.app_frame_max, width=3)\
      .grid(row=4, column=1)
    ttk.Label(self, text='Passo:').grid(row=5, column=0)
    ttk.Entry(self, textvariable=self.app_frame_step, width=3)\
      .grid(row=5, column=1)

    # Set delta T
    self.app_delta_t = StringVar(value=30)
    ttk.Label(self, text='Defina delta T:')\
      .grid(row=6, column=0, padx=5, pady=5)
    ttk.Entry(self, textvariable=self.app_delta_t, width=3)\
      .grid(row=6, column=1, padx=5, pady=5)

    # Executar algoritmos
    ttk.Button(self, text='Executar algoritmos', command=self.app_executar)\
      .grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    self.app_fig, self.app_ax = plt.subplots(figsize=(6, 4))
    self.app_canvas = FigureCanvasTkAgg(figure=self.app_fig, master=self)
    self.app_canvas.get_tk_widget().grid(row=0, rowspan=7, column=2)

    self.app_tabela = StringVar()
    ttk.Label(self, textvariable=self.app_tabela)\
      .grid(row=0, rowspan=7, column=3, padx=5, pady=5)
  
  def app_escolher_arquivo(self):
    txt_path = filedialog.askopenfilename(defaultextension='txt')
    self.app_txt_path.set(txt_path)
  
  def app_executar(self):
    # Se a string tem a extensão txt
    if '.txt' in self.app_txt_path.get().lower():
      frame_range = range(int(self.app_frame_min.get()),      # Start
                          int(self.app_frame_max.get()) + 1,  # Stop (+1 para incluir o final)
                          int(self.app_frame_step.get()))     # Step (passo)
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
      # df.to_csv('./output.csv')             # Salvando tabela em arquivo csv
      # ax.get_figure().savefig('output.png') # Salvando gráfico em um arquivo
    else:
      showwarning(title='Cuidado!!!', message='Selecione um caminho válido primeiro')
    # # Para teste apenas
    # else:
    #   data = {'FRAMES':[50, 70, 90],
    #           'FIFO':[480, 662, 833],
    #           'SC':  [488, 666, 837],
    #           'MRU': [478, 657, 824],
    #           'NUR': [484, 671, 839]}
    #   df = DataFrame(data)
    #   self.app_tabela.set(df)
    #   long_df = df.melt('FRAMES', var_name='algoritmos', value_name='acertos')
    #   self.app_ax.clear()
    #   pointplot(data=long_df,
    #             x='FRAMES',
    #             y='acertos',
    #             hue='algoritmos',
    #             ax=self.app_ax
    #             ).set(title='Algoritmos de substituição de páginas',
    #                   xlabel='Quantidade de Frames',
    #                   ylabel='Quantidade de Acertos')
    #   # ax.get_figure().savefig('output.png')
    #   self.app_canvas.draw()
      
      

#%% Main
if __name__ == '__main__':
  App().mainloop()
