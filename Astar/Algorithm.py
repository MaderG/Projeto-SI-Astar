import heapq


class priorityQueue:
    def __init__(self):
        self.estacoes = []

    def push(self, estacao, custo):
        heapq.heappush(self.estacoes, (custo, estacao))

    def pop(self):
        return heapq.heappop(self.estacoes)

    def fronteira(self):
        return sorted(self.estacoes)

    def isempty(self):
        if self.estacoes == []:
            return True
        else:
            return False



dist_direta = []
dist_real = []
linhas = []

def Makearray():  # criando matriz das distancias
    f1 = open('dist_direta.txt', 'r')
    for i in f1:
        linha = i.split(',')
        for i in range(len(linha)):
            linha[i] = float(linha[i])
        dist_direta.append(linha)
    f2 = open('dist_real', 'r')
    for i in f2:
        linha = i.split(',')
        for i in range(len(linha)):
            linha[i] = float(linha[i])
        dist_real.append(linha)

    f3 = open('linhas', 'r')
    for i in f3:
        linha = i.split(',')
        for i in range(len(linha)):
            linha[i] = str(linha[i])
        linhas.append(linha)



def g(inicio, fim):  # calculando o g(n)
    c1 = inicio.split('E')
    c1 = int(c1[1]) - 1  # coletando as coordenadas
    c2 = fim.split('E')
    c2 = int(c2[1]) - 1
    if c1 > c2:
        c1, c2 = c2, c1
    g = dist_real[c1][c2]


    return g


def h(inicio, fim):  # calculando h(n)
    c1 = inicio.split('E')
    c1 = int(c1[1]) - 1  # coletando as coordenadas
    c2 = fim.split('E')
    c2 = int(c2[1]) - 1
    if c1 > c2:
        c1, c2 = c2, c1
    h = dist_direta[c1][c2]
    return h


def estacoesadjacentes(atual, estacaoanterior):  # retorna estacoes adjacentes à atual
    s1 = atual.split('E')
    s1 = int(s1[1]) - 1
    estacaoadjacente = []
    for i in range(len(dist_real[s1])):
        if dist_real[s1][i] != 0.0 and i > s1:  # para não voltar para estação de inicio e entrar em um loop
            estacao = "E" + str(i + 1)
            estacaoadjacente.append(estacao)
        if dist_real[i][s1] != 0.0 and i <= s1:
            estacao = "E" + str(i + 1)
            estacaoadjacente.append(estacao)
    return estacaoadjacente


def astar(inicio, fim):
    caminho = {}
    distancia = {}
    q = priorityQueue()
    q.push(inicio, 0)
    distancia[inicio] = 0
    caminho[inicio] = None
    expansao = []
    Printscript(inicio, fim, caminho, distancia, expansao, q, 0)
    estacaoanterior = inicio

    while q.isempty() == False: # tira cada elemento da heap criada e expande ele
        atual = q.pop()[1]
        expansao.append(atual)

        if atual == fim:
            break

        estacaoadjacente = estacoesadjacentes(atual, estacaoanterior)

        for i, estacao in enumerate(estacaoadjacente):  #novos 'ramos' a serem visitados
            c1 = atual.split('E')
            c1 = int(c1[1]) - 1
            c2 = estacao.split('E')
            c2 = int(c2[1]) - 1
            if i == 0:
                temp = linhas[c1][c2]
            elif i <= len(estacaoadjacente) - 1:
                if temp != linhas[c1][c2]:
                    g_custo += 4
            g_custo = distancia[atual] + g(atual, estacao)
            if estacao not in distancia or g_custo < distancia[estacao]:
                distancia[estacao] = g_custo
                f_custo = g_custo + h(estacao, fim)
                q.push(estacao, f_custo)
                caminho[estacao] = atual


        Printscript(inicio, fim, caminho, distancia, expansao, q, 1)
    Printscript(inicio, fim, caminho, distancia, expansao, q, 2)


def Printscript(inicio, fim, caminho, distancia, expansao, q, nivel):
    caminhofinal = []
    i = fim

    if nivel == 0:
        print()
        print(f'Partiremos de {inicio} e iremos até {fim}\n')
    elif nivel > 0:
        print(f'\nFronteira heurística\t: {q.fronteira()}\n')
        print(f'Estacoes Expandidas\t: {expansao}', f' {len(expansao)} expansões')
        print('=======================================================')
    if nivel == 2:
        while (caminho.get(i) != None):
            caminhofinal.append(i)
            i = caminho[i]
        caminhofinal.append(inicio)
        caminhofinal.reverse()

        print('Chegamos ao destino!\n')
        print(f'Estaçoes percorridas\t {str(caminhofinal)}')


        tempo = (distancia[fim]/30) * 60

        # baldeacao
        for i in range(len(caminhofinal) - 1):
            c1 = caminhofinal[i].split('E')
            c1 = int(c1[1]) - 1
            c2 = caminhofinal[i + 1].split('E')
            c2 = int(c2[1]) - 1
            if i == 0:
                temp = linhas[c1][c2]
            if i > 0:
                if temp != linhas[c1][c2]:  # se as linhas são diferentes, fazer baldeação
                    tempo += 4
                    temp = linhas[c1][c2]
        print(f'Tempo total da viagem {tempo:.2f} minutos')




def main():
    Makearray()  # criando o mapa
    inicio = input('Digite a estacao de inicio').upper()
    fim = input('Digite a estacao de destino').upper()
    astar(inicio, fim)



if __name__ == "__main__":
    main()
