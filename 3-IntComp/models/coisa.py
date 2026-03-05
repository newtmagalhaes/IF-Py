class Coisa:

    def __init__(self, st):
        self.estado = st
        self._vivo = True

    def __repr__(self):
        # representação do objeto na forma de string
        return f'<{getattr(self, "__name__", self.__class__.__name__)}>'

    def mostraEstado(self):
        """Mostra o estado do agente. Subclasses devem sobrescrever"""
        return str(self.estado)

    def vivo(self):
        return hasattr(self, '_vivo') and self._vivo


c = Coisa(None)


def _funcao_agente_default(*entradas):
    return "Ação Default" + "\n".join(map(str, entradas))


class Agente(Coisa):
    def __init__(self, estado=None, funcaoAgente=_funcao_agente_default):
        super().__init__(estado)
        self.funcaoAgente = funcaoAgente
        self.historicoPercepcoes = []

    def percepcao(self):
        entrada = input("Entre com dados :")
        self.historicoPercepcoes.append(eval(entrada))

    def saida(self):
        return self.funcaoAgente(self.historicoPercepcoes)


class Ambiente():
    def __init__(self, estadoInicial):
        self.estado = estadoInicial
        self.objetosNoAmbiente = []
        self.agentes: list[Agente] = []

    def percepcao(self, agente):
        # Define/notifica as percepções do agente
        return None

    def adicionaAgente(self, agente):
        self.agentes.append(agente)

    def adicionaObjeto(self, obj):
        self.objetosNoAmbiente.append(obj)
