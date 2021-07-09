from grafo import Grafo

while True:
    print("Digite 'sair' para terminar a execução")
    filename = input("Insira o nome do arquivo que contém o Grafo: ")
    if filename == "sair":
        break
    try:
        g = Grafo(filename)
        g.imprime_info_distancia()
    except:
        print("Não foi possível ler o arquivo")