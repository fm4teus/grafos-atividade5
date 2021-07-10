from grafo import Grafo

while True:
    print("Digite 'sair' para terminar a execução")
    filename = input("Insira o nome do arquivo que contém o Grafo: ")
    if filename == "sair":
        break
    try:
        g = Grafo(filename)
        source, target = g.get_source_target()
        print(f'\nVértice fonte: {source}, Vértice alvo {target}\n')
        g.imprime_arestas()
        capacidade = 0
        num_cortes = int(input("\nInsira o número de arestas que compõem o corte: "))
        for i in range(num_cortes):
            aresta = int(input("Qual aresta deseja cortar: "))
            capacidade += int(g.arestas[aresta].peso)
            g.corta_aresta(aresta)
        print("\nArestas após cortes: ")    
        g.imprime_arestas()
        dist = g.dist_source_target()
        if dist<10**9:
            print(f'\nO conjunto não representa um corte\n')
        else:
            print(f'\nO conjunto representa um corte de capacidade {capacidade}\n')
    except:
        print("Não foi possível ler o arquivo")