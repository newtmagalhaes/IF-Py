class Vertice:
    def __init__(self, rotulo):
        self.rotulo = rotulo

    def __eq__(self, outro):
        return outro.rotulo == self.rotulo

    def __repr__(self):
        return self.rotulo

    def __hash__(self):
        return hash(self.rotulo)
