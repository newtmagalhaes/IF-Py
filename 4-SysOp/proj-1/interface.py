# Interface do programa
from typing import List, Tuple
from tkinter.ttk import (Progressbar, Frame, Button, Label, Entry)
from tkinter import (Tk,
                     NW,
                     Canvas,
                     IntVar,
                     DoubleVar,
                     StringVar,
                     PhotoImage)

# Constantes
WIDTH, HEIGHT = 600, 400
LOG_LIMIT = 15

# Funções
def criar_janela(name:str,
                 width : int = None,
                 height : int = None) -> Tk:
  # Janela
  win = Tk()
  win.title(name)
  if width is not None and height is not None:
    win.geometry(f'{width}x{height}')
  win.configure(background='white')

  return win


def formulario(title:str, data:List[Tuple[str, type]]) -> list:
  '''
  '''
  TYPE_MAP = {int:IntVar, str:StringVar}

  w = criar_janela(title)

  # validate = lambda: w.quit()

  entry_var_list = []
  i = 0
  for i, (var_name, tipo) in enumerate(data):
    var = TYPE_MAP[tipo](w)
    entry_var_list.append(var)

    e = Entry(w, textvariable=var)
    e.grid(row=i, column=0, padx=5, pady=5)

    l = Label(w, text=var_name)
    l.grid(row=i, column=1, padx=5, pady=5)
  
  b = Button(w, command=w.quit, text='Responder')
  b.grid(row=i+1, column=0, columnspan=2, padx=5, pady=5)
  # b.focus_set()

  w.mainloop()
  w.destroy()
  return [var.get() for var in entry_var_list]


def criar_log(window:Tk,
              log_text:StringVar,
              grid_row:int,
              grid_col:int) -> None:
  '''
  Cria um objeto tkinter.Label na window
  posicionada conforme os parametros.
  ---
  Retorna:
  uma StringVar com o qual é possível
  alterar o texto do Label
  '''
  log = Label(window, width=WIDTH/2, textvariable=log_text)
  log.grid(row=grid_row, column=grid_col, padx=10, pady=10)


def criar_tabela(window:Tk,
                 grid_row:int,
                 grid_col:int) -> StringVar:
  '''
  Cria um objeto tkinter.Label na window
  posicionada conforme os parametros.
  ---
  Retorna:
  uma StringVar com o qual é possível
  alterar o texto do Label
  '''
  pass


def criar_canvas(window:Tk,
                 grid_row:int,
                 grid_col:int) -> Canvas:

  c = Canvas(window, width=WIDTH,height=HEIGHT)
  c.grid(row=grid_row, column=grid_col, rowspan=2)
  #BACKGROUND
  bg_img = PhotoImage(file='./images/background.png')
  c.create_image(0, 0,
    image=bg_img,
    anchor=NW)
  return c




def add_message_log(new_text:str, text:StringVar, hist:List[str]):
  hist.append(new_text)
  n = len(hist)
  n_messages = n - min(LOG_LIMIT, n)
  var = '...'
  for i in range(n_messages, n):
    var += '\n' + hist[i]
    
  text.set(var)


def close(text:StringVar, hist:List[str]):
  print('fechar')
  hist.append('fechar')

  n = len(hist)
  n_messages = n - min(LOG_LIMIT, n)
  var = '...'
  for i in range(n_messages, n):
    var += '\n' + hist[i]
    
  text.set(var)


if __name__ == '__main__':
  args = [('comprimento', int),
          ('altura', int)]
  w, h = formulario('tamanho da janela', args)

  w = criar_janela('teste', w, h)

  # Log
  log_text = criar_log(w, 1, 0)
  log_hist = []

  # Botões
  button_frame = Frame(w, width=WIDTH/2)
  button_frame.grid(row=0, column=0)

  b1 = Button(button_frame,
              text='novo passageiro',
              command=lambda: add_message_log('novo passageiro criado', log_text, log_hist))
  b1.grid(row=0, column=0, padx=10, pady=10)

  b2 = Button(button_frame,
              text='close',
              command=lambda: close(log_text, log_hist))
  b2.grid(row=0, column=1, padx=10, pady=10)
  
  # tabela de objetos
  table_text = criar_tabela(w, 2, 0)

  # Canvas
  
  w.mainloop()
