# Interface do programa
from typing import List
from tkinter.ttk import (Progressbar, Frame, Button, Label)
from tkinter import (Tk,
                     Canvas,
                     StringVar)

# Constantes
WIDTH, HEIGHT = 600, 400
LOG_LIMIT = 5

# Funções
def create_window(name:str,
                  width:int,
                  height:int) -> Tk:
  # Janela
  win = Tk()
  win.title(name)
  win.geometry(f'{width}x{height}')
  win.configure(background='white')

  return win


def create_log(window:Tk,
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
  str_var = StringVar(value='log messages')
  log = Label(window, width=WIDTH/2, textvariable=str_var)
  log.grid(row=grid_row, column=grid_col)
  return str_var


def create_tabela(window:Tk,
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


def create_canvas(window:Tk,
                  grid_row:int,
                  grid_col:int) -> Canvas:
  pass

# button commands
def new_pass(text:StringVar, hist:List[str]):
  print('passageiro adicionado')
  hist.append('passageiro adicionado')
  
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
  w = create_window('teste', WIDTH, HEIGHT)

  # Log
  log_text = create_log(w, 1, 0)
  log_hist = []

  # Botões
  button_frame = Frame(w, width=WIDTH/2)
  button_frame.grid(row=0, column=0)

  b1 = Button(button_frame,
              text='novo passageiro',
              command=lambda: new_pass(log_text, log_hist))
  b1.grid(row=0, column=0, padx=10, pady=10)

  b2 = Button(button_frame,
              text='close',
              command=lambda: close(log_text, log_hist))
  b2.grid(row=0, column=1, padx=10, pady=10)
  
  # tabela de objetos
  table_text = create_tabela(w, 2, 0)

  # Canvas
  
  w.mainloop()
