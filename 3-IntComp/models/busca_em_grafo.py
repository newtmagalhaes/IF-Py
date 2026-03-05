

def bfs(grafo, inicio, meta):
    '''Busca em largura
    -------------------
    '''
    fronteira = [inicio]
    while fronteira:
        noAtual = fronteira.pop(0)
        if noAtual == meta:  # teste de meta
            return noAtual
        vizinhos = grafo.listaAdjacencias.get(noAtual)
        fronteira += vizinhos
    return "Busca não foi bem sucedida"


def bfs2(grafo, inicio, meta):
    fronteira = [[inicio]]
    visitados = set()
    while fronteira:
        # pega o primeiro caminho na fila (fronteira)
        caminho = fronteira.pop(0)

        # pega o último nó no caminho
        v = caminho[-1]

        # teste de meta
        if v == meta:
            return caminho
        # checar se o nó atual já foi visitado
        elif v not in visitados:
            # pega nos adjacentes, constroi um caminho e põe na fila
            for vizinho in grafo.listaAdjacencias.get(v):
                novoCaminho = list(caminho)
                novoCaminho.append(vizinho)
                fronteira.append(novoCaminho)

                # teste de meta
                if vizinho == meta:
                    return novoCaminho

            # coloca o vertice na lista de visitados
            visitados.add(v)


def dfs(grafo, inicio, meta, TIMEOUT=1000):
    '''Busca em Profundidade
    ------------------------
    '''
    timeout_counter = 0
    fronteira = [inicio]
    while fronteira:
        if timeout_counter > TIMEOUT:
            print('Tempo limite atingido')
            break
        v = fronteira[-1]  # verifica o último elemento adicionado
        # print("Testando ",v)
        if v == meta:
            return fronteira
        s = grafo.listaAdjacencias.get(v)  # sucessores
        if len(s) > 0:
            fronteira += s
        else:
            fronteira.pop()  # descarta o ultimo elemento
        timeout_counter += 1
    return "A busca não foi bem sucedida..."


def adjacenteNaoVisitado(visitados, lista):
    for i in lista:
        if i not in visitados:
            return i


def dfs2(grafo, inicio, meta):
    fronteira = [inicio]
    visitados = set()
    while fronteira:
        v = fronteira[-1]  # verifica o último elemento adicionado
        if v == meta:
            return fronteira
        visitados.add(v)
        # sucessor
        s = adjacenteNaoVisitado(visitados, grafo.listaAdjacencias.get(v))
        if s:
            fronteira.append(s)
        else:
            fronteira.pop()
    return "A busca não foi bem sucedida..."


if __name__ == '__main__':
    from .grafo import gr

    dfs(gr, "FORTALEZA", "HORIZONTE")
    dfs2(gr, "FORTALEZA", "HORIZONTE")

    bfs(gr, "FORTALEZA", "HORIZONTE")
    bfs2(gr, 'FORTALEZA', 'GUAIUBA')
