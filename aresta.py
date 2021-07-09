class Aresta:
    def __init__(self, de, para, peso):
        self.de = de
        self.para = para
        self.peso = peso

    def imprime(self):
        aresta = f'De: {self.de}, Para: {self.para}, Peso: {self.peso}'
        print(aresta)