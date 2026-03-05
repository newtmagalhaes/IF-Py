from graphviz import Graph

from models.vertice import Vertice


class Grafo:
    def __init__(
            self,
            vertices: list[str] = [],
            arcos: list[tuple[str, str]] = [],
            ):
        self.listaAdjacencias: dict[str, list[str]] = dict()
        self.listaVertices: set[Vertice] = set()
        for v in vertices:
            self.adicionaVertice(v)
        for o, d in arcos:
            self.adicionaArco(o, d)

    def adicionaVertice(self, rotulo):
        self.listaVertices.add(Vertice(rotulo))

    def localizaRotulo(self, rotulo):
        for i in self.listaVertices:
            if i.rotulo == rotulo:
                return i
        return -1

    def adicionaArco(self, r1: str, r2: str):
        if not self.listaAdjacencias.get(r1):
            self.listaAdjacencias[r1] = [r2]
        else:
            self.listaAdjacencias[r1].append(r2)

        if not self.listaAdjacencias.get(r2):
            self.listaAdjacencias[r2] = [r1]
        else:
            self.listaAdjacencias[r2].append(r1)

    def __repr__(self):
        return str(self.listaAdjacencias)

    def desenhaGrafo(self):
        g = Graph(
            name='grafo',
            comment='Fortaleza Metropolitana',
            strict=True,
            format='png',
        )
        for i in self.listaVertices:
            g.node(i.rotulo, i.rotulo, fontsize="10")
        for k, v in self.listaAdjacencias.items():
            for j in v:
                g.edge(k, j, dir="none")
        return g


# criando lisas de vértices e arcos
lista_vertices = [
    "FORTALEZA", "CAUCAIA", "MARACANAU", "PACATUBA", "GUAIUBA", "ITAITINGA",
    "EUSEBIO", "SAOGONCALO", "PENTECOSTE", "MARANGUAPE", "HORIZONTE", "AQUIRAZ"
]

lista_arcos = [
    ('FORTALEZA', "CAUCAIA"), ('FORTALEZA', "MARACANAU"),
    ('FORTALEZA', "PACATUBA"), ('FORTALEZA', "ITAITINGA"),
    ('FORTALEZA', "EUSEBIO"), ('CAUCAIA', "SAOGONCALO"),
    ('CAUCAIA', "PENTECOSTE"), ('MARACANAU', "MARANGUAPE"),
    ('PACATUBA', "GUAIUBA"), ('ITAITINGA', "HORIZONTE"),
    ('EUSEBIO', "AQUIRAZ"),
]

gr = Grafo(lista_vertices, lista_arcos)
g = gr.desenhaGrafo()

g.render()

