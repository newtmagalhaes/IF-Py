# Projeto 1: Problema da Montanha russa

> Entrega: 14/10/2021 

<!-- ![gif](./assets/gif_de_funcionamento) -->

|         Sumário         |
| :---------------------: |
| [Descrição](#Descrição) |
| [Interface](#Interface) |
|    [Fluxos](#Fluxos)    |
|   [Threads](#código)    |

## Descrição

Suponha a existência de uma montanha russa que contenha apenas **1** vagão com capacidade para **v** passageiros.

O vagão deverá percorrer a montanha apenas quando estiver lotado.

Suponha também que existam vários passageiros que repetidamente desejam viajar no vagão.

O vagão deverá estar desligado (_dormindo_) enquanto estiver parado na plataforma de embarque e desembarque, e só deve estar ligado (_executando_) enquanto estiver _percorrendo_ a montanha russa.

Enquanto o vagão estiver _percorrendo_ a montanha, os passageiros que estão na fila de embarque esperarão a hora de embarcar _dormindo_.

Quando o vagão chegar à plataforma, os passageiros da fila serão acordados, mas só poderão embarcar quando todos os passageiros que chegaram da viagem desembarcarem.

À medida que os passageiros desembarcam devem ir novamente para o final da fila de embarque.

Cada passageiro, antes de entrar no vagão, deverá testar se existe uma cadeira no vagão disponível para ele.

Os passageiros que estiverem viajando devem ficar _apreciando_ a paisagem durante toda a viagem, ou seja, não devem dormir.

Utilizando semáforos, implemente threads para o vagão e para os passageiros.

## Interface

A interface deverá: 
- Permitir que o usuário possa criar o vagão;

- Permitir que o usuário possa criar um passageiro a qualquer momento;

- Mostrar um log com os principais eventos de cada thread.

- Mostrar os parâmetros do vagão:
  * **v**: quantidade de cadeiras; e
  * **tv**: tempo de viagem;
  * **status** do vagão:
    - _percorrendo_ a montanha russa; ou
    - _dormindo_ na plataforma;

- Mostrar os parâmetros de cada passageiro:
  * **id**: identificador;
  * **te**: tempo de embarque; e
  * **td**: tempo de desembarque;
  * **status** de cada passageiro:
    - _dormindo_ na fila;
    - _apreciando_ a paisagem durante a viagem;
    - _embarcando_ no vagão; ou
    - _desembarcando_ do vagão.

## Fluxos

Serão explicados os procedimentos a serem realizados em cada etapa da aplicação.

### inicialização

1. - [x] Criar janela;
  
> Discutir entre fazer isso logo abaixo ou apenas criar a caixa de diálogo antes da janela principal;
2. - [x] Posicionar componentes visuais (desativados até resolver a caixa de diálogo);
     - [ ] a fila e o passeio;
     - [ ] botão para adicionar passageiro;
     - [x] botão para encerrar expediente (desalocar variáveis e encerrar o programa);
     - [x] log com as chamadas realizadas;
  
3. - [x] Abrir caixa de diálogo:
     - [x] pedir dados do vagão (_devem ser estritamente positivos_):
       - **v**: quantidade de vagas;
       - **tv**: tempo de viagem;
     - [ ] recusar dados inválidos;
     - [x] instanciar vagão com dados válidos (_status:dormindo_); 

### execução

- [x] funcionalidade do botão para adicionar passageiros (demais threads executando enquanto isso):
  - [x] Abrir caixa de diálogo:
     - [x] pedir dados do passageiro (_devem ser estritamente positivos_):
       - **te**: tempo de embarque;
       - **td**: tempo de desembarque;
     - [ ] recusar dados inválidos;
     - [x] instanciar passageiro com dados válidos e adicionar ao fim da fila (_status:dormindo_);

Durante a execução, ocorrem 2 fluxos de passageiros:
- da fila para o vagão;
- do vagão para a fila.

#### Fila de Passageiros

A fila de passageiros pode ser implementada com uma lista.
- [x] cada passageiro terá um método para entrar e sair da fila;
- [x] será preciso um _mutex_ para operações que alterem a lista; (contido no vagão)
  > é possível que seja preciso definir um tipo (`Fila = list[Passageiro]`) compreendendo essa lista e o _mutex_.

#### Vagão

O vagão tbm deverá possuir uma estrutura semelhante à fila.
- [x] cada passageiro terá um método para entrar e sair do vagão;
- [x] será preciso um _mutex_ para operações que alterem a ocupação do vagão;
  > O _mutex_ e a lista de passageiros dentro do vagão podem ser implementados dentro da classe `Vagão`.

### Encerramento

- [x] funcionalidade do botão de fim do expediente:
  - [x] desembarcar passageiros quando o vagão estiver na plataforma (momento de embarque ou desembarque);
  - [x] bloquear embarque;
  - [x] desalocar passageiros;
  - [x] desalocar vagão;
  - [x] fechar janela;

## código

[aqui](./proj_types.py)

### Inicialização

Momento para criar a janela e constantes:
```Python
# Mutex para ações de leitura e escrita na fila e no vagão
MUTEX = Lock()

# Passageiros no vagão aguardando o passeio começar
AGUARDAR_EMBARQUE = Semaphore(0)

criar_janela()

# A janela fornece os valores de N_VAGAS e T_VIAGEM
vagao = Vagao(N_VAGAS, T_VIAGEM)

# Semáforos do Vagão:

# Permite a transição de passageiros entre fila e vagão
vagao.pode_embarcar = Semaphore(1)
vagao.pode_desembarcar = Semaphore(0)

# Permite o vagão começar o passeio
vagao.pode_passear = Semaphore(0)

# Indicando se o vagão está vazio após desembarque
vagao.esta_vago = Semaphore(0)

# Indica que a aplicação ainda está executando
vagao._executando = True
```

### Vagão

```Python
def run(self):
    while self._executando:
      self.pode_passear.acquire()

      self.iniciar_passeio()
      for _ in range(self._vagas):
        AGUARDAR_EMBARQUE.release()
      
      self.realizar_passeio()
      for _ in range(self._vagas):
        self.pode_desembarcar.release()
      
      self.vagao_livre.acquire()
      self.pode_embarcar.release()
    
    print('Vagão voltando para garagem')
```

### Passageiros

```Python
def run(self):
    with MUTEX:
      self.entrar_na_fila()
    
    while self._vagao._executando:
      if self == self._fila[0]:
        self._vagao.pode_embarcar.acquire()
        # Se o vagão não estiver mais executando após o release
        if not self._vagao._executando:
          break

        with MUTEX:
          self.sair_da_fila()
          self.embarcar()
          if self._vagao.esta_cheio():
            self._vagao.pode_passear.release()
          else:
            self._vagao.pode_embarcar.release()
        
        AGUARDAR_EMBARQUE.acquire()
        while self._vagao.status == 'percorrendo':
          self.apreciar_paisagem()
        self._vagao.pode_desembarcar.acquire()
        with MUTEX:
          self.desembarcar()
          self.entrar_na_fila()
          if self._vagao.esta_vago():
            self._vagao.vagao_livre.release()
      else:
        sleep(2)
    
    with MUTEX:
      self.sair_da_fila()
      print(f'Passageiro {self.id} indo embora')
```
