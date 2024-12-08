import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# TODO: Função para carregar um grafo a partir de um arquivo CSV contendo arestas.
def carregar_grafo_de_arestas(caminho_arquivo, coluna_origem, coluna_destino):
    """Carrega um grafo a partir de um arquivo CSV contendo arestas."""
    arestas = pd.read_csv(caminho_arquivo)
    print("Colunas carregadas:", arestas.columns)  # Depuração para verificar colunas
    grafo = nx.from_pandas_edgelist(arestas, source=coluna_origem, target=coluna_destino)
    return grafo

# TODO: Função para plotar um grafo, com a opção de amostrar nós para grafos grandes.
def plotar_grafo(grafo, titulo, amostra=None):
    """Plota o grafo (com amostragem opcional para grafos grandes)."""
    if amostra and len(grafo.nodes) > amostra:
        print(f"Grafo grande detectado! Amostrando {amostra} nós para visualização...")
        nos_amostrados = list(grafo.nodes)[:amostra]
        grafo = grafo.subgraph(nos_amostrados)
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(grafo, seed=42)
    nx.draw(grafo, pos, node_size=10, edge_color="orange", node_color="blue", with_labels=False, alpha=1) 
    plt.title(titulo, fontsize=15)
    plt.show()

#alpha = opacidade
#edge = aresta / node = vertice

# TODO: Função para plotar a distribuição de graus dos vértices de um grafo.
def plotar_distribuicao_grau(grafo, titulo):
    """Plota a distribuição dos graus dos vértices."""
    graus = [grau for _, grau in grafo.degree()]
    plt.figure(figsize=(8, 6))
    plt.hist(graus, bins=30, color="blue", edgecolor="black", alpha=0.7)
    plt.title(f"Distribuição de Graus - {titulo}", fontsize=15)
    plt.xlabel("Grau")
    plt.ylabel("Frequência")
    plt.show()

# TODO: Dicionário que configura os caminhos dos arquivos de entrada e suas colunas.
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

# TODO: Bloco principal para processar os grafos das redes sociais e exibir análises.
# Processar grafos das redes sociais
resultados = {}
for rede in ["deezer", "facebook", "lastfm"]:
    print(f"\n{'=' * 60}")
    print(f"Processando a Rede: {rede.capitalize()}")
    print(f"{'=' * 60}\n")

    # TODO: Carregar o grafo da rede social atual.
    grafo = carregar_grafo_de_arestas(
        arquivos_dados[rede]["caminho"],
        arquivos_dados[rede]["coluna_origem"],
        arquivos_dados[rede]["coluna_destino"]
    )
    print(f"Grafo carregado com sucesso: {len(grafo.nodes):,} nós, {len(grafo.edges):,} arestas.\n")

    # TODO: Plotar o grafo (Questão 1A).
    # Questão 1A: Plotar o grafo
    print(f"{'-' * 40}")
    print(f"Questão 1A: Plotando o Grafo")
    print(f"{'-' * 40}")
    plotar_grafo(grafo, f"Grafo da Rede {rede.capitalize()}", amostra=220)

    # TODO: Calcular o grau médio dos vértices (Questão 1B).
    # Questão 1B: Calcular o grau médio
    print(f"\n{'-' * 40}")
    print(f"Questão 1B: Grau Médio")
    print(f"{'-' * 40}")
    distribuicao_grau = [grau for _, grau in grafo.degree()]
    grau_medio = sum(distribuicao_grau) / len(distribuicao_grau)
    print(f"Grau médio: {grau_medio:.2f}")

    # TODO: Plotar a distribuição de graus (Questão 1C).
    # Questão 1C: Plotar a distribuição de graus
    print(f"\n{'-' * 40}")
    print(f"Questão 1C: Distribuição de Graus")
    print(f"{'-' * 40}")
    plotar_distribuicao_grau(grafo, f"Rede {rede.capitalize()}")

    # TODO: Calcular o número de componentes conexos e o tamanho do maior componente (Questão 1D).
    # Questão 1D: Componentes conexos
    print(f"\n{'-' * 40}")
    print(f"Questão 1D: Componentes Conexos")
    print(f"{'-' * 40}")
    num_componentes = nx.number_connected_components(grafo)
    print(f"Número de componentes conexos: {num_componentes}")
    tamanhos_componentes = [len(c) for c in nx.connected_components(grafo)]
    print(f"Tamanho do maior componente: {max(tamanhos_componentes):,} nós.")

    # TODO: Questão 1E: Distância média na maior componente
    print(f"\n{'-' * 40}")
    print(f"Questão 1E: Distância Média na Maior Componente")
    print(f"{'-' * 40}")
    maior_componente = max(nx.connected_components(grafo), key=len)
    subgrafo_maior = grafo.subgraph(maior_componente)

    # Verifica se o subgrafo é conexo
    if nx.is_connected(subgrafo_maior):
        distancia_media = nx.average_shortest_path_length(subgrafo_maior)
        print(f"Distância média na maior componente: {distancia_media:.2f}")
    else:
        print("O maior componente não é conexo; não é possível calcular a distância média.")


    # TODO: Identificar arestas pontes (Questão 1F).
    # Questão 1F: Arestas pontes
    print(f"\n{'-' * 40}")
    print(f"Questão 1F: Arestas Pontes")
    print(f"{'-' * 40}")
    arestas_pontes = list(nx.bridges(grafo))
    print(f"Número de arestas pontes: {len(arestas_pontes):,}\n")

    # TODO: Salvar os resultados para o resumo final.
    # Salvar resultados
    resultados[rede] = {
        "grau_medio": grau_medio,
        "numero_componentes": num_componentes,
        "tamanho_maior_componente": max(tamanhos_componentes),
        # "distancia_media_maior_componente": distancia_media,
        "numero_arestas_pontes": len(arestas_pontes),
    }

# TODO: Exibir um resumo final de todas as redes processadas.
# Exibir resumo final
print(f"\n{'=' * 60}")
print("Resumo Final de Todas as Redes")
print(f"{'=' * 60}")
for rede, analise in resultados.items():
    print(f"\nRede: {rede.capitalize()}")
    print(f"{'-' * 40}")
    for metrica, valor in analise.items():
        print(f"{metrica.replace('_', ' ').capitalize()}: {valor}")
    print(f"{'-' * 40}")

# todo:#################################################################################################################
# todo:#################################################################################################################
# todo:
# todo:     QUESTÃO 2 A BAIXO:
# todo:     QUESTÃO 2 A BAIXO:
# todo:     QUESTÃO 2 A BAIXO:
# todo:
# todo:#################################################################################################################
# todo:#################################################################################################################


# TODO: Bloco dedicado à análise da rede Scientometrics (Questão 2).
# Questão 2: Ciência Cientométrica
print(f"\n{'=' * 60}")
print("Processando o Grafo de Citações: Scientometrics")
print(f"{'=' * 60}\n")

# TODO: Carregar o grafo de citações como orientado.
# Carregar o grafo como orientado
grafo_citacoes = nx.read_edgelist(
    arquivos_dados["scientometrics"]["caminho"],
    create_using=nx.DiGraph()
)
print(f"Grafo carregado com sucesso: {len(grafo_citacoes.nodes):,} nós, {len(grafo_citacoes.edges):,} arestas.\n")

# TODO: Calcular a densidade do grafo (Questão 2A).
# Questão 2A: Densidade do Grafo
print(f"{'-' * 40}")
print("Questão 2A: Densidade do Grafo")
print(f"{'-' * 40}")
densidade = nx.density(grafo_citacoes)
print(f"Densidade do Grafo: {densidade:.4f}\n")

# TODO: Calcular o grau médio de entrada e saída (Questão 2B).
# Questão 2B: Grau dos Vértices
print(f"{'-' * 40}")
print("Questão 2B: Grau dos Vértices")
print(f"{'-' * 40}")
grau_entrada = sum(dict(grafo_citacoes.in_degree()).values()) / len(grafo_citacoes.nodes)
grau_saida = sum(dict(grafo_citacoes.out_degree()).values()) / len(grafo_citacoes.nodes)
print(f"Grau médio de entrada: {grau_entrada:.2f}")
print(f"Grau médio de saída: {grau_saida:.2f}\n")

# TODO: Identificar componentes fortemente e fracamente conectados (Questão 2C).
# Questão 2C: Componentes Conexos
print(f"{'-' * 40}")
print("Questão 2C: Componentes Conexos")
print(f"{'-' * 40}")
componentes_fortes = nx.number_strongly_connected_components(grafo_citacoes)
componentes_fracos = nx.number_weakly_connected_components(grafo_citacoes)
print(f"Número de componentes fortemente conectados: {componentes_fortes}")
print(f"Número de componentes fracamente conectados: {componentes_fracos}\n")

# TODO: Verificar ciclos e calcular caminhos mais curtos na maior componente (Questão 2D).
# Questão 2D: Caminhos e Ciclos
print(f"{'-' * 40}")
print("Questão 2D: Caminhos e Ciclos")
print(f"{'-' * 40}")
print("Verificando a presença de ciclos...")
ciclos = list(nx.simple_cycles(grafo_citacoes))
print(f"Número de ciclos encontrados: {len(ciclos)}")

print("\nCalculando a média dos caminhos mais curtos...")
try:
    distancia_media = nx.average_shortest_path_length(grafo_citacoes)
    print(f"Média dos caminhos mais curtos: {distancia_media:.2f}")
except nx.NetworkXError:
    print("O grafo não é fortemente conectado; não é possível calcular a distância média.\n")

# TODO: Exibir centralidade de grau normalizada e grau absoluto (Questão 2E).
# Questão 2E: Centralidade de Grau
print(f"{'-' * 40}")
print("Questão 2E: Centralidade de Grau")
print(f"{'-' * 40}")

# TODO: Calcular e exibir centralidade de grau normalizada.
# Centralidade de Grau Normalizada
centralidade_grau_entrada = nx.in_degree_centrality(grafo_citacoes)
centralidade_grau_saida = nx.out_degree_centrality(grafo_citacoes)

print("\nTop 5 nós por centralidade de grau (entrada - normalizada):")
for no, valor in sorted(centralidade_grau_entrada.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {valor:.4f}")

print("\nTop 5 nós por centralidade de grau (saída - normalizada):")
for no, valor in sorted(centralidade_grau_saida.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {valor:.4f}")

# TODO: Calcular e exibir grau absoluto.
# Grau Absoluto
graus_entrada = dict(grafo_citacoes.in_degree())
graus_saida = dict(grafo_citacoes.out_degree())

print("\nTop 5 nós por grau de entrada (absoluto):")
for no, grau in sorted(graus_entrada.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {grau}")

print("\nTop 5 nós por grau de saída (absoluto):")
for no, grau in sorted(graus_saida.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Nó {no}: {grau}")

# TODO:
# TODO:
# TODO: HTML
# TODO:
# TODO:

# TODO: Gerar um arquivo HTML aprimorado e mais organizado para exibir os resultados
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados da Análise</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            background: #1a1a2e;
            color: #eaeaea;
        }
        .sidebar {
            width: 300px;
            background: #16213e;
            padding: 20px;
            box-shadow: 4px 0 10px rgba(0, 0, 0, 0.5);
            color: #fff;
        }
        .sidebar h1 {
            font-size: 1.5em;
            margin-bottom: 20px;
            border-bottom: 2px solid #e94560;
            padding-bottom: 10px;
        }
        .main-content {
            flex: 1;
            padding: 20px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .panel {
            background: #0f3460;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            flex: 1 1 calc(50% - 20px);
            min-width: 300px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .panel:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
        }
        .panel h2 {
            margin-top: 0;
            color: #e94560;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            background: #16213e;
            margin: 5px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .metric span {
            font-weight: bold;
        }
        footer {
            text-align: center;
            padding: 20px;
            background: #16213e;
            color: #eaeaea;
        }
    </style>
</head>
<body>
<div class="sidebar">
    <h1>Resultados</h1>
    <p>Este painel apresenta os resultados das análises de grafos, organizados em categorias.</p>
</div>
<div class="main-content">
"""

# Adicionar um painel para cada rede social
for rede, analise in resultados.items():
    html_content += f"""
    <div class="panel">
        <h2>Rede: {rede.capitalize()}</h2>
    """
    for metrica, valor in analise.items():
        html_content += f"""
        <div class="metric">
            <span>{metrica.replace('_', ' ').capitalize()}:</span>
            <span>{valor}</span>
        </div>
        """
    html_content += "</div>"

# TODO: Adicionar painel de Scientometrics
html_content += """
<div class="panel">
    <h2>Scientometrics</h2>
    <div class="metric">
        <span>Densidade do Grafo:</span>
        <span>{:.4f}</span>
    </div>
    <div class="metric">
        <span>Grau Médio de Entrada:</span>
        <span>{:.2f}</span>
    </div>
    <div class="metric">
        <span>Grau Médio de Saída:</span>
        <span>{:.2f}</span>
    </div>
    <div class="metric">
        <span>Componentes Fortemente Conectados:</span>
        <span>{}</span>
    </div>
    <div class="metric">
        <span>Componentes Fracamente Conectados:</span>
        <span>{}</span>
    </div>
    <div class="metric">
        <span>Ciclos Encontrados:</span>
        <span>{}</span>
    </div>
""".format(densidade, grau_entrada, grau_saida, componentes_fortes, componentes_fracos, len(ciclos))

html_content += "</div>"

# Fechar o HTML
html_content += """
</div>
<footer>
    <p>&copy; 2024 Análise de Grafos. Todos os direitos reservados.</p>
</footer>
</body>
</html>
"""



# TODO: Salvar o HTML em um arquivo
with open("resultados.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Arquivo HTML gerado: resultados.html")
