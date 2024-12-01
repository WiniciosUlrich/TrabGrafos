import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def carregar_grafo_de_arestas(caminho_arquivo, coluna_origem, coluna_destino):
    """Carrega um grafo a partir de um arquivo CSV contendo arestas."""
    arestas = pd.read_csv(caminho_arquivo)
    print("Colunas carregadas:", arestas.columns)  # Depuração para verificar colunas
    grafo = nx.from_pandas_edgelist(arestas, source=coluna_origem, target=coluna_destino)
    return grafo

def plotar_grafo(grafo, titulo, amostra=None):
    """Plota o grafo (com amostragem opcional para grafos grandes)."""
    if amostra and len(grafo.nodes) > amostra:
        print(f"Grafo grande detectado! Amostrando {amostra} nós para visualização...")
        nos_amostrados = list(grafo.nodes)[:amostra]
        grafo = grafo.subgraph(nos_amostrados)
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(grafo, seed=42)
    nx.draw(grafo, pos, node_size=10, edge_color="gray", node_color="blue", with_labels=False, alpha=0.7)
    plt.title(titulo, fontsize=15)
    plt.show()

def plotar_distribuicao_grau(grafo, titulo):
    """Plota a distribuição dos graus dos vértices."""
    graus = [grau for _, grau in grafo.degree()]
    plt.figure(figsize=(8, 6))
    plt.hist(graus, bins=30, color="blue", edgecolor="black", alpha=0.7)
    plt.title(f"Distribuição de Graus - {titulo}", fontsize=15)
    plt.xlabel("Grau")
    plt.ylabel("Frequência")
    plt.show()

# Configurar os caminhos dos arquivos
arquivos_dados = {
    "deezer": {
        "caminho": "deezer_europe_edges.csv",
        "coluna_origem": "node_1",
        "coluna_destino": "node_2"
    },
    "facebook": {
        "caminho": "musae_facebook_edges.csv",
        "coluna_origem": "id_1",
        "coluna_destino": "id_2"
    },
    "lastfm": {
        "caminho": "lastfm_asia_edges.csv",
        "coluna_origem": "node_1",
        "coluna_destino": "node_2"
    },
    "scientometrics": {
        "caminho": "scientometrics.net"
    }
}


# Processar grafos das redes sociais
resultados = {}
for rede in ["deezer", "facebook", "lastfm"]:
    print(f"\n{'='*60}")
    print(f"Processando a Rede: {rede.capitalize()}")
    print(f"{'='*60}\n")

    grafo = carregar_grafo_de_arestas(
        arquivos_dados[rede]["caminho"],
        arquivos_dados[rede]["coluna_origem"],
        arquivos_dados[rede]["coluna_destino"]
    )
    print(f"Grafo carregado com sucesso: {len(grafo.nodes):,} nós, {len(grafo.edges):,} arestas.\n")

    # Questão 1A: Plotar o grafo
    print(f"{'-'*40}")
    print(f"Questão 1A: Plotando o Grafo")
    print(f"{'-'*40}")
    plotar_grafo(grafo, f"Grafo da Rede {rede.capitalize()}", amostra=500)

    # Questão 1B: Calcular o grau médio
    print(f"\n{'-'*40}")
    print(f"Questão 1B: Grau Médio")
    print(f"{'-'*40}")
    distribuicao_grau = [grau for _, grau in grafo.degree()]
    grau_medio = sum(distribuicao_grau) / len(distribuicao_grau)
    print(f"Grau médio: {grau_medio:.2f}")

    # Questão 1C: Plotar a distribuição de graus
    print(f"\n{'-'*40}")
    print(f"Questão 1C: Distribuição de Graus")
    print(f"{'-'*40}")
    plotar_distribuicao_grau(grafo, f"Rede {rede.capitalize()}")

    # Questão 1D: Componentes conexos
    print(f"\n{'-'*40}")
    print(f"Questão 1D: Componentes Conexos")
    print(f"{'-'*40}")
    num_componentes = nx.number_connected_components(grafo)
    print(f"Número de componentes conexos: {num_componentes}")
    tamanhos_componentes = [len(c) for c in nx.connected_components(grafo)]
    print(f"Tamanho do maior componente: {max(tamanhos_componentes):,} nós.")

    # # Questão 1E: Distância média na maior componente
    # print(f"\n{'-'*40}")
    # print(f"Questão 1E: Distância Média na Maior Componente")
    # print(f"{'-'*40}")
    # maior_componente = max(nx.connected_components(grafo), key=len)
    # subgrafo_maior = grafo.subgraph(maior_componente)
    # distancia_media = nx.average_shortest_path_length(subgrafo_maior)
    # print(f"Distância média na maior componente: {distancia_media:.2f}")

    # Questão 1F: Arestas pontes
    print(f"\n{'-'*40}")
    print(f"Questão 1F: Arestas Pontes")
    print(f"{'-'*40}")
    arestas_pontes = list(nx.bridges(grafo))
    print(f"Número de arestas pontes: {len(arestas_pontes):,}\n")

    # Salvar resultados
    resultados[rede] = {
        "grau_medio": grau_medio,
        "numero_componentes": num_componentes,
        "tamanho_maior_componente": max(tamanhos_componentes),
        # "distancia_media_maior_componente": distancia_media,
        "numero_arestas_pontes": len(arestas_pontes),
    }

# Exibir resumo final
print(f"\n{'='*60}")
print("Resumo Final de Todas as Redes")
print(f"{'='*60}")
for rede, analise in resultados.items():
    print(f"\nRede: {rede.capitalize()}")
    print(f"{'-'*40}")
    for metrica, valor in analise.items():
        print(f"{metrica.replace('_', ' ').capitalize()}: {valor}")
    print(f"{'-'*40}")


# todo:#################################################################################################################
# todo:#################################################################################################################
# todo:
# todo:     QUESTÃO 2 A BAIXO:
# todo:     QUESTÃO 2 A BAIXO:
# todo:     QUESTÃO 2 A BAIXO:
# todo:
# todo:#################################################################################################################
# todo:#################################################################################################################


# Questão 2: Ciência Cientométrica

print(f"\n{'='*60}")
print("Processando o Grafo de Citações: Scientometrics")
print(f"{'='*60}\n")

# Carregar o grafo como orientado
grafo_citacoes = nx.read_edgelist(
    arquivos_dados["scientometrics"]["caminho"],
    create_using=nx.DiGraph()
)
print(f"Grafo carregado com sucesso: {len(grafo_citacoes.nodes):,} nós, {len(grafo_citacoes.edges):,} arestas.\n")

# Questão 2A: Densidade do Grafo
print(f"{'-'*40}")
print("Questão 2A: Densidade do Grafo")
print(f"{'-'*40}")
densidade = nx.density(grafo_citacoes)
print(f"Densidade do Grafo: {densidade:.4f}\n")

# Questão 2B: Grau dos Vértices
print(f"{'-'*40}")
print("Questão 2B: Grau dos Vértices")
print(f"{'-'*40}")
grau_entrada = sum(dict(grafo_citacoes.in_degree()).values()) / len(grafo_citacoes.nodes)
grau_saida = sum(dict(grafo_citacoes.out_degree()).values()) / len(grafo_citacoes.nodes)
print(f"Grau médio de entrada: {grau_entrada:.2f}")
print(f"Grau médio de saída: {grau_saida:.2f}\n")

# Questão 2C: Componentes Conexos
print(f"{'-'*40}")
print("Questão 2C: Componentes Conexos")
print(f"{'-'*40}")
componentes_fortes = nx.number_strongly_connected_components(grafo_citacoes)
componentes_fracos = nx.number_weakly_connected_components(grafo_citacoes)
print(f"Número de componentes fortemente conectados: {componentes_fortes}")
print(f"Número de componentes fracamente conectados: {componentes_fracos}\n")

# Questão 2D: Caminhos e Ciclos
print(f"{'-'*40}")
print("Questão 2D: Caminhos e Ciclos")
print(f"{'-'*40}")
print("Verificando a presença de ciclos...")
ciclos = list(nx.simple_cycles(grafo_citacoes))
print(f"Número de ciclos encontrados: {len(ciclos)}")

print("\nCalculando a média dos caminhos mais curtos...")
try:
    distancia_media = nx.average_shortest_path_length(grafo_citacoes)
    print(f"Média dos caminhos mais curtos: {distancia_media:.2f}")
except nx.NetworkXError:
    print("O grafo não é fortemente conectado; não é possível calcular a distância média.\n")

# Questão 2E: Centralidade de Grau
print(f"{'-'*40}")
print("Questão 2E: Centralidade de Grau")
print(f"{'-'*40}")

# Centralidade de Grau Normalizada
centralidade_grau_entrada = nx.in_degree_centrality(grafo_citacoes)
centralidade_grau_saida = nx.out_degree_centrality(grafo_citacoes)

print("\nTop 5 nós por centralidade de grau (entrada - normalizada):")
for no, valor in sorted(centralidade_grau_entrada.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {valor:.4f}")

print("\nTop 5 nós por centralidade de grau (saída - normalizada):")
for no, valor in sorted(centralidade_grau_saida.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {valor:.4f}")

# Grau Absoluto
graus_entrada = dict(grafo_citacoes.in_degree())
graus_saida = dict(grafo_citacoes.out_degree())

print("\nTop 5 nós por grau de entrada (absoluto):")
for no, grau in sorted(graus_entrada.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {grau}")

print("\nTop 5 nós por grau de saída (absoluto):")
for no, grau in sorted(graus_saida.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {grau}")