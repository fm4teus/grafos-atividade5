from os import sendfile
from aresta import Aresta

def read(self, filename):
    self.num_arestas = 0
    self.arestas = []
    self.vertices_sucessores = {}
    self.vertices_antecessores = {}
    with open(filename) as file_object:
        contents = file_object.readlines()
        for line in contents:
            self.num_arestas += 1
            values = line.split()
            origem = values[0]
            fim = values[1]
            peso = values[2]
            self.arestas.append(Aresta(origem, fim, peso))
            self.vertices_sucessores.setdefault(origem,[]).append(fim)
            self.vertices_antecessores.setdefault(fim,[]).append(origem)

class Grafo:
    def __init__(self, filename):
        read(self, filename)
        self.vertices = self.calcula_num_vertices()
        self.num_vertices = len(self.vertices)
        self.densidade = self.num_arestas/(self.num_vertices*(self.num_vertices-1))
        self.dist = self.floyd_warshall()
        self.excentricidade_exterior, self.excentricidade_interior = self.excentricidade()
        self.raio_exterior, self.raio_interior = self.raio()
        self.diametro_exterior, self.diametro_interior = self.diametro()
        self.centro_exterior, self.centro_interior = self.centro()
        self.periferia_exterior, self.periferia_interior = self.periferia()
        self.centroide_exterior, self.centroide_interior = self.centroide()
    
    def sumario(self):
        print("\nO grafo analisado contém: ")
        print(f'{self.num_arestas} Arestas')
        print(f'{self.num_vertices} Vertices')
        print(f'Densidade de {self.densidade*100}%\n')

    def imprime(self):
        print("\n   ---ARESTAS---   ")
        for aresta in self.arestas:
            aresta.imprime()
        print("\n    ---VÉRTICES---    ")
        for vertice in self.vertices:
            self.sucessores(vertice)

    def calcula_num_vertices(self):
        vertices = []
        for ant in self.vertices_antecessores:
            if ant not in vertices:
                vertices.append(ant)
        for suc in self.vertices_sucessores:
            if suc not in vertices:
                vertices.append(suc)
        return vertices

    def grau(self, vertice):
        grau_entrada = len(self.vertices_antecessores[vertice]) if vertice in self.vertices_antecessores else 0
        grau_saida = len(self.vertices_sucessores[vertice]) if vertice in self.vertices_sucessores else 0
        print(f'\nGrau de entrada: {grau_entrada}')
        print(f'Grau de saída: {grau_saida}\n')

    def sucessores(self, vertice):
        if vertice not in self.vertices_sucessores:
            print(f'O vértice {vertice} não possui sucessores!')
        else:
            msg = f'Sucessores de {vertice}: '
            for sucessor in self.vertices_sucessores[vertice]:
                msg += f'{sucessor}, '
            print(msg)

    def antecessores(self, vertice):
        if vertice not in self.vertices_antecessores:
            print(f'O vértice {vertice} não possui antecessores!')
        else:
            msg = f'Antecessores de {vertice}: '
            for antecessor in self.vertices_antecessores[vertice]:
                msg += f'{antecessor}, '
            print(msg)

    def floyd_warshall(self):
        dist = [[]]
        for i in range(self.num_vertices):
            dist.append([])
            for j in range(self.num_vertices):
                dist[i].append(10**9)
        for vertice in self.vertices:
            v = int(vertice)-1
            dist[v][v] = 0
        for aresta in self.arestas:
            origem = int(aresta.de)-1
            fim = int(aresta.para)-1
            peso = int(aresta.peso)
            dist[origem][fim] = peso
        for k in range(0,self.num_vertices):
            for i in range(0,self.num_vertices):
                for j in range(0,self.num_vertices):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    def imprime_dist(self):
        linha = "V |"
        bar = "__|"
        for i in range(0, self.num_vertices):
            linha += f'{i+1}  '
            bar+='___'
        print(linha)
        print(bar)
        for i in range(0, self.num_vertices):
            linha = f'{i+1} |'
            for j in range(0, self.num_vertices):
                linha += f'{str(self.dist[i][j])}  '
            print(linha)

    def excentricidade(self):
        excentricidade_exterior = []
        excentricidade_interior = []
        for i in range(0, self.num_vertices):
            maior_exterior = self.dist[i][0]
            maior_interior = self.dist[0][i]
            for j in range(0, self.num_vertices):
                if self.dist[i][j] > maior_exterior:
                    maior_exterior = self.dist[i][j]
                if self.dist[j][i] > maior_interior:
                    maior_interior = self.dist[j][i]
            excentricidade_exterior.append(maior_exterior)
            excentricidade_interior.append(maior_interior)
        return (excentricidade_exterior, excentricidade_interior)

    def raio(self):
        raio_exterior = min(self.excentricidade_exterior)
        raio_interior = min(self.excentricidade_interior)
        return (raio_exterior, raio_interior)
    
    def diametro(self):
        diametro_exterior = max(self.excentricidade_exterior)
        diametro_interior = max(self.excentricidade_interior)
        return (diametro_exterior, diametro_interior)

    def centro(self):
        centro_exterior = []
        centro_interior = []
        for index, value in enumerate(self.excentricidade_exterior):
            if value == self.raio_exterior:
                centro_exterior.append(index+1)
        for index, value in enumerate(self.excentricidade_interior):
            if value == self.raio_interior:
                centro_interior.append(index+1)
        return (centro_exterior, centro_interior)
    
    def periferia(self):
        periferia_exterior = []
        periferia_interior = []
        for index, value in enumerate(self.excentricidade_exterior):
            if value == self.diametro_exterior:
                periferia_exterior.append(index+1)
        for index, value in enumerate(self.excentricidade_interior):
            if value == self.diametro_interior:
                periferia_interior.append(index+1)
        return (periferia_exterior, periferia_interior)

    def centroide(self):
        soma_exterior = []
        soma_interior = []
        for i in range(0,self.num_vertices):
            soma = 0
            soma_exterior.append(sum(self.dist[i]))
            for j in range(0,self.num_vertices):
                soma += self.dist[j][i]
            soma_interior.append(soma)
        
        centroide_exterior = []
        soma_min = min(soma_exterior)
        for index, value in enumerate(soma_exterior):
            if value == soma_min:
                centroide_exterior.append(index+1)

        centroide_interior = []
        soma_min = min(soma_interior)
        for index, value in enumerate(soma_interior):
            if value == soma_min:
                centroide_interior.append(index+1)

        return (centroide_exterior, centroide_interior) 

    def imprime_info_distancia(self):
        print('')
        print(f'Excentricidade exterior: {self.excentricidade_exterior}')
        print(f'raio exterior: {self.raio_exterior}')
        print(f'diametro exterior: {self.diametro_exterior}')
        print(f'centro exterior: {self.centro_exterior}')
        print(f'centroide exterior: {self.centroide_exterior}')
        print(f'periferia exterior: {self.periferia_exterior}')
        print('')
        print(f'Excentricidade interior: {self.excentricidade_interior}')
        print(f'raio interior: {self.raio_interior}')
        print(f'diametro interior: {self.diametro_interior}')
        print(f'centro interior: {self.centro_interior}')
        print(f'centroide interior: {self.centroide_interior}')
        print(f'periferia interior: {self.periferia_interior}')