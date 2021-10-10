# Projeto 1: Problema da Montanha russa

> Entrega: 14/10/2021 

<!-- ![gif](./assets/gif_de_funcionamento) -->

|         Sumário          |
| :----------------------: |
| [Descrição](#Descrição)  |
| [Interface](#Interface)  |
|    [Fluxos](#Fluxos)     |
| [Threads](#Pseudocódigo) |

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

1. - [ ] Criar janela;
  
> Discutir entre fazer isso logo abaixo ou apenas criar a caixa de diálogo antes da janela principal;
2. - [ ] Posicionar componentes visuais (desativados até resolver a caixa de diálogo);
     - [ ] a fila e o passeio;
     - [ ] botão para adicionar passageiro;
     - [ ] botão para encerrar expediente (desalocar variáveis e encerrar o programa);
     - [ ] log com as chamadas realizadas;
  
3. - [ ] Abrir caixa de diálogo:
     - [ ] pedir dados do vagão (_devem ser estritamente positivos_):
       - **v**: quantidade de vagas;
       - **tv**: tempo de viagem;
     - [ ] recusar dados inválidos;
     - [ ] instanciar vagão com dados válidos (_status:dormindo_); 

### execução

- [ ] funcionalidade do botão para adicionar passageiros (demais threads executando enquanto isso):
  - [ ] Abrir caixa de diálogo:
     - [ ] pedir dados do passageiro (_devem ser estritamente positivos_):
       - **te**: tempo de embarque;
       - **td**: tempo de desembarque;
     - [ ] recusar dados inválidos;
     - [ ] instanciar passageiro com dados válidos e adicionar ao fim da fila (_status:dormindo_);

Durante a execução, ocorrem 2 fluxos de passageiros:
- da fila para o vagão;
- do vagão para a fila.

#### Fila de Passageiros

A fila de passageiros pode ser implementada com uma lista.
- [ ] cada passageiro terá um método para entrar e sair da fila;
- [ ] será preciso um _mutex_ para operações que alterem a lista;
  > é possível que seja preciso definir um tipo (`Fila`) compreendendo essa lista e o _mutex_.

#### Vagão

O vagão tbm deverá possuir uma estrutura semelhante à fila.
- [ ] cada passageiro terá um método para entrar e sair do vagão;
- [ ] será preciso um _mutex_ para operações que alterem a ocupação do vagão;
  > O _mutex_ e a lista de passageiros dentro do vagão podem ser implementados dentro da classe `Vagão`.

### Encerramento

- [ ] funcionalidade do botão de fim do expediente:
  - [ ] desembarcar passageiros quando o vagão estiver na plataforma (momento de embarque ou desembarque);
  - [ ] bloquear embarque;
  - [ ] desalocar passageiros;
  - [ ] desalocar vagão;
  - [ ] fechar janela;

## Pseudocódigo

### Inicialização

Momento para criar a janela e constantes:
```Python
criar_janela()
vagao = criar_vagao()

# Permite a transição de passageiros entre fila e vagão
embarcar = Semaphore(1)
desembarcar = Semaphore(0)

# Passageiros no vagão aguardando o passeio começar
aguardar = Semaphore(0)

# Permite o vagão começar o passeio
passear = Semaphore(0)

# Indicando se o vagão está vazio após desembarque
vago = Semaphore(0)

# Mutex para ações de leitura e escrita na fila e no vagão
mutex = Lock()

# Indica que a aplicação ainda está executando
executando = True
```

### Vagão

```Python
while executando:
  DOWN(passear)
  começar_passeio() # Set status como 'percorrendo'
  for i in vagao.n_vagas:
    # Libera passageiros para apreciar a paisagem
    UP(aguardar)
  realizar_passeio() # Set status como 'dormindo'
  for i in vagao.n_vagas:
    UP(desembarcar)
  DOWN(vago) 
  UP(embarcar)
```

### Passageiros

```Python
entrar_na_fila()
while True:
  if self in fila.inicio():
    DOWN(embarcar)
    DOWN(mutex)
    embarcar_no_vagao() # Altera a fila e o vagão
    if vagao.esta_cheio():
      UP(passear)
    else:
      UP(embarcar)
    UP(mutex)
    DOWN(aguardar)
    while vagao.status == 'percorrendo':
      apreciar_paisagem()
    DOWN(desembarcar)
    DOWN(mutex)
    desembarcar_do_vagao()
    entrar_na_fila()
    if vagao.esta_vago():
      UP(vago)
    UP(mutex)
  else:
    # aguarda um momento para conferir de novo
    # se está no início da fila ou não
    sleep(1)
```
