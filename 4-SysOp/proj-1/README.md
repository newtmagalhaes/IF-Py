# Projeto 1: Problema da Montanha russa

> Entrega: 14/10/2021 

<!-- ![gif](./assets/gif_de_funcionamento) -->

|         Sumário          |
| :----------------------: |
| [Descrição](##Descrição) |
| [Interface](##Interface) |
|    [Fluxos](##Fluxos)    |

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

- [ ] funcionalidade do botão para adicionar passageiros:
  - [ ] Abrir caixa de diálogo (demais threads executando enquanto isso):
     - [ ] pedir dados do passageiro (_devem ser estritamente positivos_):
       - **te**: tempo de embarque;
       - **td**: tempo de desembarque;
     - [ ] recusar dados inválidos;
     - [ ] instanciar passageiro com dados válidos e adicionar ao fim da fila (_status:dormindo_);

- [ ] funcionalidade do botão de fim do expediente:
  - [ ] desembarcar passageiros quando o vagão estiver na plataforma (momento de embarque ou desembarque);
  - [ ] bloquear embarque;
  - [ ] desalocar passageiros;
  - [ ] desalocar vagão;
  - [ ] fechar janela;

#### Fila de Passageiros

#### Embarque 

#### Desembarque

### Encerramento
