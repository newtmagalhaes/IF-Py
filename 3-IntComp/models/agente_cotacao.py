from .coisa import Agente, Ambiente


# Nosso agente inteligente vai decidir entre comprar e vender dólares 
# aqui estamos encapsulando o conhecimento a respeito do assunto
def funcaoAgenteCompraDolar(media, valor):
    ##
    # REGRAS/TABELA DE DECISÃO
    ###
    if valor >= media:
        return False, valor, media
    else:
        return True, valor, media


class AgenteCambio(Agente):

    def __init__(self, estadoInicial=None, funcaoAgente=None):
        super().__init__(estadoInicial, funcaoAgente)
        self.observacao = 0
        self.mediaAtual = 0
        self.medias = []

    def atualizaEstado(self, valor):
        self.observacao += 1
        if self.observacao == 1:
            self.mediaAtual = valor
        else:
            self.mediaAtual = (
                self.mediaAtual
                + (valor - self.mediaAtual)/(self.observacao + 1)
            )
        self.estado.append(valor)
        self.medias.append(self.mediaAtual)

    def percepcao(self, valorAtual):
        self.atualizaEstado(valorAtual)

    def saida(self):
        return self.funcaoAgente(self.medias[-1], self.estado[-1])


ac = AgenteCambio([], funcaoAgenteCompraDolar)


class AgenteCambioDesempenho(AgenteCambio):
    def __init__(self, estadoInicial, funcaoAgente=None, saldoR=0, saldoD=0):
        super().__init__(estadoInicial, funcaoAgente)
        self.saldoReal = saldoR
        self.saldoDolar = saldoD
        self.evolucaoReal = []

    def comprar(self):
        # Ação comprar
        if self.saldoReal > 0:
            self.saldoDolar += self.saldoReal/self.estado[-1]
            self.saldoReal = 0

    def vender(self):
        # Ação vender
        if self.saldoDolar > 0:
            self.saldoReal += self.saldoDolar * self.estado[-1]
            self.saldoDolar = 0
        self.evolucaoReal.append(self.saldoReal)

    def desempenho(self):
        # lucrototal
        print("desempenho")
        return self.evolucaoReal[-1] - self.evolucaoReal[0]


class AmbienteFinanceiro(Ambiente):
    
    def __init__(self, estadoInicial):
        self.agentes: list[AgenteCambioDesempenho]
        super().__init__(estadoInicial)

    def percepcao(self, agentes):
        for i in self.estado:
            for ag in agentes:
                ag.percebe(i)
        return

    def executaAmbiente(self):
        for gst in self.estado:
            for ag in self.agentes:
                ag.atualizaEstado(gst)
                acaoComprar = ag.saida()
                if acaoComprar[0] is True:
                    ag.comprar()
                else:
                    ag.vender()

    def desemPenhoAgentes(self):
        desempenho = []
        for i, ag in enumerate(self.agentes):
            desempenho.append((i, ag.desempenho()))
        return desempenho


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # botando nosso agente pra trabalhar
    ag = AgenteCambioDesempenho([], funcaoAgenteCompraDolar, 1000, 0)
    amb = AmbienteFinanceiro(y)
    amb.adicionaAgente(ag)
    amb.executaAmbiente()
    desempenho = amb.desemPenhoAgentes()
    print("Desempenho geral: (Agente, Lucro)",desempenho)

    ##

    # evolucao em real
    plt.figure(figsize=(18, 3))
    plt.style.use('dark_background')
    x2 = list(range(len(ag.evolucaoReal)))
    plt.plot(x2, ag.evolucaoReal, color='r')
    plt.xlabel('Transações Efetuadas')
    plt.ylabel('Saldo em Reais')
    plt.title('Evolução do Investimento no Período')
    plt.grid(color='white', linestyle='--', linewidth=0.5)
    plt.show()
