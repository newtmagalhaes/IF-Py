# Arquivo principal
from time import sleep
from typing import List
from threading import Thread
from tkinter.ttk import Frame
from tkinter import (Tk, NW,
                     Button,
                     Canvas,
                     StringVar,
                     IntVar,
                     PhotoImage)
# arquivos na mesma pasta
from proj_types import Vagao, Passageiro
from interface import (formulario,
                       add_message_log,
                       criar_janela,
                       criar_log,
                       criar_tabela,
                       criar_canvas)

# Constantes
WIDTH, HEIGHT = 540, 360

# Funções para botões
def criar_vagao(log_text:StringVar, log_hist:List[str]) -> Vagao:
  args = [('número de vagas', int),
          ('tempo de viagem (em segundos)', int)]
  vagas, t_viagem = formulario('dados do vagão', args)
  v = Vagao(vagas,
            t_viagem,
            log_text,
            log_hist,
            add_message_log)
  #VAGAO
  # canvas.create_image(0,0,
  #   image=PhotoImage(file='./images/Vagao.png'),
  #   anchor=NW)
  v.start()
  return v

def criar_passageiro(id:IntVar,
                     carrinho:Vagao,
                     fila:List[Passageiro],
                     log_text:StringVar,
                     log_hist:List[str]):
  args = [('tempo de embarque (em segundos)', int),
          ('tempo de desembarque (em segundos)', int)]
  # print('formulário de passageiro')
  embarque, desembarque = formulario('dados do passageiro', args)
  
  # print('instanciando passageiro')
  p = Passageiro(str(id.get()),
                 embarque,
                 desembarque,
                 carrinho,
                 fila,
                 log_text,
                 log_hist, 
                 add_message_log)

  id.set(id.get() + 1)
  # janela.destroy()
  # print('passageiro criado no botão')
  p.start()
  return p

def stop(v:Vagao, f:List[Passageiro], w:Tk) -> None:
  v.desligar()
  v.join()
  for p in f:
    p.join()
  w.quit()

if __name__ == '__main__':
  # Globais
  w = criar_janela('Montanha Russa')
  log_hist = ['inicio do log']
  log_text = StringVar(value=log_hist[0])
  last_id = IntVar(value=1)
  f:List[Passageiro] = []
  # v = Vagao(1, 5, log_text, log_hist, add_message_log)
  # p = Passageiro('00', 5, 5, v, f, log_text, log_hist, add_message_log)

  # Log
  criar_log(w, log_text, 1, 0)

  # Botões
  button_frame = Frame(w, width=WIDTH/2)
  button_frame.grid(row=0, column=0)

  b1 = Button(button_frame,
              text='stop',
              background='#AA0000',
              command=lambda: Thread(target=stop, args=(v, f, w)).start())
  b1.grid(row=0, column=0, padx=10, pady=10)

  b2 = Button(button_frame,
              text='Novo Passageiro',
              background='#0000AA',
              command=lambda: criar_passageiro(last_id, v, f, log_text, log_hist))
  b2.grid(row=0, column=1, padx=10, pady=10)
  
  # tabela de objetos
  # table_text = criar_tabela(w, 2, 0)

  # Canvas
  # c = criar_canvas(w, 0, 2)
  # Vagão
  v = criar_vagao(log_text, log_hist)

  w.mainloop()
  add_message_log('fim do log', log_text, log_hist)
  sleep(3)
  w.destroy()
