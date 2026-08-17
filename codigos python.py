# =========================================================
# Script para gerar um schema.sql a partir de CSVs
# =========================================================

import csv   # biblioteca para ler arquivos CSV
import os    # biblioteca para trabalhar com pastas e arquivos

# -------------------------------------------------
# Caminhos usados no script
# -------------------------------------------------

# Pasta onde estão os arquivos CSV de origem
PASTA_CSV = r'C:\Users\Wpere\Downloads\meu_projeto\csv'

# Local onde o arquivo schema.sql será criado
ARQUIVO_SQL = r'C:\Users\Wpere\Downloads\meu_projeto\schema.sql'


# -------------------------------------------------
# Abre o arquivo SQL de saída para escrita
# -------------------------------------------------

with open(ARQUIVO_SQL, 'w', encoding='utf-8') as sql:

    # Lista todos os arquivos da pasta, em ordem alfabética
    arquivos_da_pasta = sorted(os.listdir(PASTA_CSV))

    # Contador para saber quantas tabelas foram criadas
    total_tabelas = 0

    # -------------------------------------------------
    # Percorre cada arquivo encontrado na pasta
    # -------------------------------------------------

    for nome_arquivo in arquivos_da_pasta:

        # Processa apenas arquivos que terminam com .csv
        if nome_arquivo.lower().endswith('.csv'):

            # Monta o caminho completo do arquivo CSV
            caminho_csv = os.path.join(PASTA_CSV, nome_arquivo)

            # Usa o nome do arquivo (sem extensão) como nome da tabela
            nome_tabela = os.path.splitext(nome_arquivo)[0]

            # -------------------------------------------------
            # Abre o arquivo CSV para leitura
            # -------------------------------------------------

            with open(
                caminho_csv,
                mode='r',
                encoding='utf-8-sig',
                newline=''
            ) as arquivo_csv:

                # Cria o leitor de CSV
                leitor = csv.reader(arquivo_csv)

                # Lê a primeira linha do CSV, que contém os nomes das colunas
                colunas = next(leitor)

                # -------------------------------------------------
                # Monta a definição de cada coluna como TEXT
                # -------------------------------------------------

                definicoes_colunas = []

                for nome_coluna in colunas:
                    definicoes_colunas.append(f'"{nome_coluna}" TEXT')

                # Junta todas as colunas separadas por vírgula
                texto_colunas = ',\n    '.join(definicoes_colunas)

                # -------------------------------------------------
                # Monta o comando CREATE TABLE completo
                # -------------------------------------------------

                comando_create_table = (
                    f'CREATE TABLE "{nome_tabela}" (\n'
                    f'    {texto_colunas}\n'
                    f');\n\n'
                )

                # Escreve o comando no arquivo schema.sql
                sql.write(comando_create_table)

                # Atualiza o contador de tabelas criadas
                total_tabelas += 1


# -------------------------------------------------
# Mensagem final, exibida no terminal
# -------------------------------------------------

print('Processo finalizado com sucesso.')
print(f'Arquivo gerado: {ARQUIVO_SQL}')
print(f'Total de tabelas criadas: {total_tabelas}')



#==================================================================================================

# --------------------------------------------------------------------------------------------------
# Questão 3.2 - Validação 
# Qual o total de linhas somadas das seguintes tabelas: customers, orders, order_items e payments? 
# --------------------------------------------------------------------------------------------------

import csv
import os


# Pasta onde estão os arquivos CSV
PASTA_CSV = r'C:\Users\Wpere\Downloads\meu_projeto\csv'

# Lista com os nomes das tabelas que você quer somar
TABELAS = ['customers', 'orders', 'order_items', 'payments']


# Variável para acumular o total de linhas
total_geral = 0


# Percorre cada tabela da lista
for nome_tabela in TABELAS:

    # Monta o caminho completo do arquivo CSV
    caminho_csv = os.path.join(PASTA_CSV, f'{nome_tabela}.csv')

    # Abre o arquivo CSV
    with open(caminho_csv, 'r', encoding='utf-8-sig', newline='') as arquivo:

        # Cria o leitor do CSV
        leitor = csv.reader(arquivo)

        # Pula a primeira linha (cabeçalho)
        next(leitor)

        # Conta quantas linhas restaram (linhas de dados)
        quantidade_linhas = sum(1 for linha in leitor)

        # Mostra o resultado individual de cada tabela
        print(f'{nome_tabela}: {quantidade_linhas} linhas')

        # Soma ao total geral
        total_geral += quantidade_linhas


# Mostra o resultado final
print(f'\nTotal de linhas somadas: {total_geral}')

# --------------------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------------------
# Questao 6 - Previsão de demanda 
# --------------------------------------------------------------------------------------------------
# O Sr. Almir está furioso. No último verão, o estoque de "Coletes Salva-Vidas" acabou em 3 meses, e a empresa perdeu milhares de reais em vendas. Por outro lado, compraram "Âncoras" demais e elas estão enferrujando no galpão. Gabriel Santos, o Tech Lead, disse que não dá mais para confiar no "feeling". Ele quer um modelo preditivo que diga exatamente quantas unidades venderemos no próximo mês para ajustar as compras com fornecedores. 
# Premissas obrigatórias: 
# O período de treino deve incluir dados até 31/12/2025. 
# O período de teste deve ser o primeiro trimestre de 2026. 
# A previsão deve ser feita em base mensal. 
# Considere apenas o produto: "Bússola de Bordo 702" 
# --------------------------------------------------------------------------------------------------
# Tarefa: 
# --------------------------------------------------------------------------------------------------
# 1. Utilize os datasets products.csv, product_variants, orders.csv e order_items.csv para criar um dataset unificado que facilite a criação do modelo preditivo. 
# 2. Construa um modelo baseline simples, utilizando: Média móvel dos últimos 3 meses de vendas (considerando apenas dados anteriores à data prevista). 
# 3. Gere a previsão mensal de vendas para o primeiro trimestre de 2026. 
# 4. Compare as previsões com os valores reais do período de teste utilizando a métrica: MAE (Mean Absolute Error) 
# 5. Responda objetivamente: 
#      a. O baseline é adequado para esse produto? 
#      b. Cite uma limitação desse método. 
# --------------------------------------------------------------------------------------------------

# ============================================================
# Codigo ajustado devido a itens com nomes iguais e IDs diferentes
# ============================================================
# 1 – CONFIGURAÇÃO
# ============================================================
import csv
import sqlite3
from datetime import datetime

# diretório onde estão os CSVs
DIR_CSV = r"C:\Users\Wpere\Downloads\meu_projeto\csv"

# arquivos
ARQ_PRODUCTS        = f"{DIR_CSV}\\products.csv"
ARQ_VARIANTS        = f"{DIR_CSV}\\product_variants.csv"
ARQ_ORDERS          = f"{DIR_CSV}\\orders.csv"
ARQ_ORDER_ITEMS     = f"{DIR_CSV}\\order_items.csv"

# banco SQLite (arquivo temporário)
DB_FILE = "nautical.db"

# ============================================================
# 2 – FUNÇÕES AUXILIARES
# ============================================================
def ler_csv(caminho):
    """Lê um CSV e devolve lista de dicionários (sem pandas)."""
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def criar_tabela(conn, nome, colunas):
    """
    Cria tabela SQLite a partir de lista de nomes de colunas.
    Todas as colunas são TEXT (simples para este exercício).
    """
    cols_sql = ", ".join([f'"{c}" TEXT' for c in colunas])
    sql = f'CREATE TABLE IF NOT EXISTS "{nome}" ({cols_sql});'
    conn.execute(sql)

def inserir_lote(conn, nome, linhas):
    """Insere várias linhas de uma vez (executemany)."""
    if not linhas:
        return
    colunas = linhas[0].keys()
    placeholders = ", ".join(["?"] * len(colunas))
    sql = f'INSERT INTO "{nome}" ({",".join(colunas)}) VALUES ({placeholders});'
    valores = [tuple(l[c] for c in colunas) for l in linhas]
    conn.executemany(sql, valores)

def data_para_mes(data_str):
    """Converte 'yyyy-mm-dd...' para (ano, mês) – formato dd/mm/aaaa usado nas saídas."""
    dt = datetime.strptime(data_str[:10], "%Y-%m-%d")
    return dt.year, dt.month

def mes_para_texto(ano, mes):
    """Retorna 'mm/aaaa'."""
    return f"{mes:02d}/{ano}"

# ============================================================
# 3 – CRIAÇÃO DO BANCO E IMPORTAÇÃO DOS CSVs
# ============================================================
conn = sqlite3.connect(DB_FILE)

# products
produtos = ler_csv(ARQ_PRODUCTS)
criar_tabela(conn, "products", produtos[0].keys())
inserir_lote(conn, "products", produtos)

# product_variants
variantes = ler_csv(ARQ_VARIANTS)
criar_tabela(conn, "product_variants", variantes[0].keys())
inserir_lote(conn, "product_variants", variantes)

# orders
pedidos = ler_csv(ARQ_ORDERS)
criar_tabela(conn, "orders", pedidos[0].keys())
inserir_lote(conn, "orders", pedidos)

# order_items
itens = ler_csv(ARQ_ORDER_ITEMS)
criar_tabela(conn, "order_items", itens[0].keys())
inserir_lote(conn, "order_items", itens)

conn.commit()


# ============================================================
# 4 – IDENTIFICAÇÃO DOS IDs DO PRODUTO ALVO
# ============================================================
NOME_ALVO = "Bússola de Bordo 702"
cur = conn.cursor()
cur.execute(
    "SELECT id FROM products WHERE name = ?",
    (NOME_ALVO,)
)
ids_alvo = [row[0] for row in cur.fetchall()]          # → ['74', '240']
print(f"IDs encontrados para '{NOME_ALVO}': {ids_alvo}")

# manter o produto “asdf” (IDs 187 e 342) – ele já está na base,
# portanto não precisamos removê‑lo. Apenas sinalizamos nos
# rankings quando aparecer.


# ============================================================
# 5 – MAPEAMENTO VARIANTE → PRODUCT_ID
# ============================================================
cur.execute(
    "SELECT id, product_id FROM product_variants WHERE product_id IN ({seq})".format(
        seq=",".join(["?"] * len(ids_alvo))
    ),
    ids_alvo
)
variantes_alvo = {row[0]: row[1] for row in cur.fetchall()}


# ============================================================
# 6 – DICIONÁRIO (order_id → data) – apenas data de criação
# ============================================================
cur.execute("SELECT id, created_at FROM orders")
pedido_data = {row[0]: data_para_mes(row[1]) for row in cur.fetchall()}


# ============================================================
# 7 – AGREGAR QUANTIDADE VENDIDA POR MÊS
# ------------------------------------------------------------
#   a) CENÁRIO COMBINADO  (soma dos dois IDs)
#   b) CENÁRIO SEPARADO  (cada ID tratado individualmente)
# ============================================================
# estrutura: {(ano, mes): quantidade}
quant_comb = {}
quant_sep  = {pid: {} for pid in ids_alvo}

for item in itens:
    var_id = item.get("product_variant_id") or item.get("variant_id")
    prod_id = variantes_alvo.get(var_id)
    if not prod_id:
        continue                     # variante de outro produto

    order_id = item["order_id"]
    mes = pedido_data.get(order_id)
    if not mes:
        continue

    qtd = int(item["quantity"])

    # combinado
    quant_comb[mes] = quant_comb.get(mes, 0) + qtd

    # separado
    d = quant_sep[prod_id]
    d[mes] = d.get(mes, 0) + qtd


# ============================================================
# 8 – PREPARAR SÉRIE COMPLETA (preencher meses sem venda)
# ------------------------------------------------------------
def completar_serie(dicionario, ano_fim=2026, mes_fim=3):
    """Garante que todos os meses de 2020‑01 até ano_fim‑mes_fim existam."""
    # menor data presente (pode ser antes de 2020, mas o enunciado começa em 2020)
    if not dicionario:
        return {}
    menor = min(dicionario.keys())
    ano, mes = menor
    serie = {}
    while (ano, mes) <= (ano_fim, mes_fim):
        serie[(ano, mes)] = dicionario.get((ano, mes), 0)
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1
    return serie


serie_comb = completar_serie(quant_comb)
serie_sep  = {pid: completar_serie(q) for pid, q in quant_sep.items()}


# ============================================================
# 9 – FUNÇÃO DE PREVISÃO (média móvel de 3 meses)
# ------------------------------------------------------------
def previsao_media_movel(serie):
    """Retorna dicionário {mes: previsão} para todos os meses a partir do 4.º."""
    meses = sorted(serie.keys())
    previsoes = {}
    for i in range(3, len(meses)):
        mes_atual = meses[i]
        tres_anteriores = meses[i-3:i]
        soma = sum(serie[m] for m in tres_anteriores)
        previsoes[mes_atual] = soma // 3          # inteiro, sem casas decimais
    return previsoes


prev_comb = previsao_media_movel(serie_comb)
prev_sep  = {pid: previsao_media_movel(s) for pid, s in serie_sep.items()}


# ============================================================
# 10 – CÁLCULO DO MAE (Mean Absolute Error) – teste = Jan/Fev/Mar 2026
# ------------------------------------------------------------
MESES_TREINO = [(2025, 12), (2025, 11), (2025, 10)]   # apenas exemplo; o código usa tudo antes de 2026
MESES_TREINO = [(y, m) for y in range(2020, 2026) for m in range(1, 13) if (y, m) < (2026, 1)]
MESES_TREINO = [(y, m) for y, m in MESES_TREINO if (y, m) < (2026, 1)]

MES_TREINO = [(2025, 12), (2025, 11), (2025, 10)]  # não usado, mantido por clareza


def mae(real, pred, meses_teste):
    erro = 0
    n = 0
    for mes in meses_teste:
        erro += abs(real.get(mes, 0) - pred.get(mes, 0))
        n += 1
    return erro // n if n else 0


meses_teste = [(2026, 1), (2026, 2), (2026, 3)]

mae_comb = mae(serie_comb, prev_comb, meses_teste)
mae_sep  = {pid: mae(serie_sep[pid], prev_sep[pid], meses_teste) for pid in ids_alvo}


# ============================================================
# 11 – EXIBIÇÃO DOS RESULTADOS
# ------------------------------------------------------------
def imprimir_cenario(titulo, serie, previsao, mae_val):
    print("\n=== " + titulo + " ===")
    print("Mês       | Real | Previsão")
    print("-" * 30)
    for mes in meses_teste:
        txt = mes_para_texto(*mes)
        real = serie.get(mes, 0)
        prev = previsao.get(mes, 0)
        print(f"{txt} | {real:5d} | {prev:8d}")
    print(f"\nMAE do baseline: {mae_val}")
    soma_prev = sum(previsao.get(m, 0) for m in meses_teste)
    print(f"Soma total prevista (1.º tri/2026): {soma_prev}")


# CENÁRIO COMBINADO
imprimir_cenario(
    "CENÁRIO COMBINADO (IDs 74 + 240)",
    serie_comb,
    prev_comb,
    mae_comb
)

# CENÁRIO SEPARADO – cada ID
for pid in ids_alvo:
    imprimir_cenario(
        f"CENÁRIO SEPARADO – Produto ID {pid}",
        serie_sep[pid],
        prev_sep[pid],
        mae_sep[pid]
    )

# ------------------------------------------------------------
# 12 – OBSERVAÇÃO SOBRE O PRODUTO “asdf”
# ------------------------------------------------------------
# O produto “asdf” (IDs 187 e 342) permanece na base e aparecerá
# nos rankings caso seja um dos mais semelhantes ao “Motor de Popa 1949”.
# Não o removemos; apenas sinalizamos nos relatórios:
def marcar_suspeito(nome):
    return "  <-- produto suspeito (verificar cadastro)" if nome.lower() == "asdf" else ""

# Exemplo de uso (não faz parte do cálculo de demanda):
print("\nObservação: ao gerar rankings de similaridade, inclua a mensagem acima para o produto 'asdf'.")


# ============================================================
# 13 – LIMPEZA
# ============================================================
conn.close()

# ============================================================
# Questao 7 - Sistema de recomendação 
# ============================================================

# Cenário 
# A Marina percebeu que clientes que compram lanchas quase sempre esquecem de levar a defensa (proteção lateral). Ela quer implementar uma vitrine de "Quem comprou isso, também levou..." no site.  
# Como não temos ferramentas de Big Data caras, você precisará criar um motor de recomendação, baseado na similaridade de compra dos clientes.  
# Identificar qual produto deve ser recomendado junto ao item “Motor de Popa 1949”, com base na similaridade de comportamento de compra dos clientes. 

# ============================================================
# Tarefa: 
# ============================================================

# 1. Crie uma matriz de interação Usuário × Produto obedecendo às regras abaixo: 
#     a. Linhas: id_cliente 
#     b. Colunas: id_produto 
#     c. Valor da célula: 
#     d. 1 se o cliente comprou ao menos uma vez o produto 
#     e. 0 caso contrário 
#     f. Ignore a quantidade comprada (presença/ ausência apenas) 
# --------------------------------------------------------------------------------------------------
# 2. Cálculo de Similaridade entre Produtos 
# --------------------------------------------------------------------------------------------------
#     a. Calcule a Similaridade de Cosseno (Cosine Similarity) entre os vetores dos produtos 
#     b. A similaridade deve ser calculada produto × produto, com base nos clientes que compraram cada item 
# --------------------------------------------------------------------------------------------------
# 3. Ranking de Produtos Similares 
# --------------------------------------------------------------------------------------------------
#     a. Considere o produto “Motor de Popa 1949” como item de referência 
#     b. Gere um ranking com os nomes dos 5 produtos mais similares a ele 
#     c. Desconsidere o próprio motor no ranking 
# --------------------------------------------------------------------------------------------------


import csv
import math

# ============================================================
# CONFIGURACAO: diretorio onde estao os arquivos CSV
# ============================================================
DIRETORIO_CSV = r"C:\Users\Wpere\Downloads\meu_projeto\csv"


# ============================================================
# PASSO 1: Funcao simples para ler qualquer arquivo CSV
# ============================================================
def ler_csv(caminho):
    with open(caminho, newline='', encoding='utf-8') as arquivo:
        return list(csv.DictReader(arquivo))


products = ler_csv(DIRETORIO_CSV + "\\products.csv")
product_variants = ler_csv(DIRETORIO_CSV + "\\product_variants.csv")
orders = ler_csv(DIRETORIO_CSV + "\\orders.csv")
order_items = ler_csv(DIRETORIO_CSV + "\\order_items.csv")


# ============================================================
# PASSO 2: Lista de nomes de produtos SUSPEITOS
# (nao sao removidos do calculo, apenas sinalizados no ranking
# para avaliacao posterior da area responsavel)
# ============================================================
nomes_suspeitos = {"asdf"}


# ============================================================
# PASSO 3: Criar dois dicionarios de identificacao do produto
# - id_para_nome: usado no cenario JUNTO (agrupa por nome,
#   juntando IDs duplicados como 74/240, 29/317, etc.)
# - id_para_id_proprio: usado no cenario SEPARADO (mantem
#   cada ID como um item individual)
# ============================================================
id_para_nome = {}
id_para_id_proprio = {}

for produto in products:
    id_produto = produto['id']
    id_para_nome[id_produto] = produto['name']
    id_para_id_proprio[id_produto] = id_produto


# ============================================================
# PASSO 4: Ligar cada VARIANTE ao ID do PRODUTO
# ============================================================
variante_para_id_produto = {}

for variante in product_variants:
    id_variante = variante['id']
    id_produto = variante['product_id']
    if id_produto in id_para_nome:
        variante_para_id_produto[id_variante] = id_produto


# ============================================================
# PASSO 5: Ligar cada PEDIDO ao CLIENTE
# ============================================================
pedido_para_cliente = {}

for pedido in orders:
    pedido_para_cliente[pedido['id']] = pedido['customer_id']


# ============================================================
# PASSO 6: Funcao que constroi a MATRIZ USUARIO-ITEM
# Recebe o dicionario de identificacao (nome ou id proprio)
# Formato: matriz[cliente][item] = quantidade comprada
# ============================================================
def construir_matriz(dicionario_identificacao):
    matriz = {}

    for item in order_items:
        id_pedido = item['order_id']
        id_variante = item['variant_id']
        quantidade = int(float(item['quantity']))

        if id_pedido not in pedido_para_cliente:
            continue
        if id_variante not in variante_para_id_produto:
            continue

        cliente = pedido_para_cliente[id_pedido]
        id_produto = variante_para_id_produto[id_variante]
        identificador_item = dicionario_identificacao[id_produto]

        if cliente not in matriz:
            matriz[cliente] = {}

        if identificador_item not in matriz[cliente]:
            matriz[cliente][identificador_item] = 0

        matriz[cliente][identificador_item] += quantidade

    return matriz


# ============================================================
# PASSO 7: Funcao que calcula a similaridade de cosseno
# entre dois itens, com base nas compras de todos os clientes
# ============================================================
def calcular_similaridade_cosseno(item_a, item_b, matriz):
    soma_multiplicacao = 0
    soma_quadrado_a = 0
    soma_quadrado_b = 0

    for cliente in matriz:
        valor_a = matriz[cliente].get(item_a, 0)
        valor_b = matriz[cliente].get(item_b, 0)

        soma_multiplicacao += valor_a * valor_b
        soma_quadrado_a += valor_a * valor_a
        soma_quadrado_b += valor_b * valor_b

    if soma_quadrado_a == 0 or soma_quadrado_b == 0:
        return 0

    denominador = math.sqrt(soma_quadrado_a) * math.sqrt(soma_quadrado_b)
    return soma_multiplicacao / denominador


# ============================================================
# PASSO 8: Funcao que gera o ranking de similaridade
# de um item contra todos os outros itens da matriz
# ============================================================
def gerar_ranking(item_alvo, matriz):
    todos_os_itens = set()
    for cliente in matriz:
        for item in matriz[cliente]:
            todos_os_itens.add(item)

    if item_alvo not in todos_os_itens:
        return None

    lista_similaridades = []
    for item in todos_os_itens:
        if item == item_alvo:
            continue
        similaridade = calcular_similaridade_cosseno(item_alvo, item, matriz)
        lista_similaridades.append((item, similaridade))

    lista_similaridades.sort(key=lambda x: x[1], reverse=True)
    return lista_similaridades


# ============================================================
# PASSO 9: CENARIO JUNTO (produtos agrupados por nome)
# ============================================================
produto_alvo_nome = "Motor de Popa 1949"

matriz_junto = construir_matriz(id_para_nome)
ranking_junto = gerar_ranking(produto_alvo_nome, matriz_junto)

print("=== CENARIO JUNTO (produtos agrupados por nome) ===")

if ranking_junto is None:
    print("Produto nao encontrado:", produto_alvo_nome)
else:
    for item, similaridade in ranking_junto[:10]:
        if item in nomes_suspeitos:
            aviso = "  [ATENCAO: nome de produto suspeito - enviar para avaliacao da area responsavel]"
        else:
            aviso = ""
        print(item, "-> similaridade:", round(similaridade, 2), aviso)

    produto_recomendado_junto = ranking_junto[0][0]
    valor_similaridade_junto = round(ranking_junto[0][1], 2)

    print("")
    print("Produto com MAIOR similaridade (cenario JUNTO):", produto_recomendado_junto, "- similaridade:", valor_similaridade_junto)

    if produto_recomendado_junto in nomes_suspeitos:
        print("OBSERVACAO: o produto recomendado possui nome suspeito. Validar cadastro antes de usar na vitrine.")


# ============================================================
# PASSO 10: CENARIO SEPARADO (cada ID tratado individualmente)
# ============================================================
matriz_separado = construir_matriz(id_para_id_proprio)

ids_do_produto_alvo = []
for produto in products:
    if produto['name'] == produto_alvo_nome:
        ids_do_produto_alvo.append(produto['id'])

print("")
print("=== CENARIO SEPARADO (cada ID tratado individualmente) ===")

for id_alvo in ids_do_produto_alvo:
    print("")
    print("Produto ID:", id_alvo)
    ranking_separado = gerar_ranking(id_alvo, matriz_separado)

    if ranking_separado is None:
        print("  Nenhuma venda encontrada para este ID.")
        continue

    for item_id, similaridade in ranking_separado[:5]:
        nome_do_item = id_para_nome.get(item_id, "Desconhecido")
        if nome_do_item in nomes_suspeitos:
            aviso = "  [ATENCAO: nome de produto suspeito - enviar para avaliacao da area responsavel]"
        else:
            aviso = ""
        print(" ", nome_do_item, "(ID", item_id, ") -> similaridade:", round(similaridade, 2), aviso)

    id_recomendado = ranking_separado[0][0]
    nome_recomendado = id_para_nome.get(id_recomendado, "Desconhecido")
    valor_similaridade_separado = round(ranking_separado[0][1], 2)

    print("  Produto com MAIOR similaridade para o ID", id_alvo, ":", nome_recomendado, "(ID", id_recomendado, ") - similaridade:", valor_similaridade_separado)

    if nome_recomendado in nomes_suspeitos:
        print("  OBSERVACAO: o produto recomendado possui nome suspeito. Validar cadastro antes de usar na vitrine.")



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

# Script para exportar resultados SQL para CSV

# ============================================================
# Script para exportar os resultados das questoes para CSV
# Esses CSVs serao usados como fonte de dados no Power BI
# ============================================================
import sqlite3
import csv
import os

# Caminho do banco ja criado nas etapas anteriores
CAMINHO_BANCO = "nautical.db"

# Pasta onde os CSVs de saida serao salvos
PASTA_SAIDA = r"C:\Users\Wpere\Downloads\meu_projeto\power_bi_export"

# Cria a pasta de saida, caso nao exista
os.makedirs(PASTA_SAIDA, exist_ok=True)

conn = sqlite3.connect(CAMINHO_BANCO)
cursor = conn.cursor()


# ============================================================
# Funcao generica: roda uma query e salva o resultado em CSV
# ============================================================
def exportar_para_csv(nome_arquivo, comando_sql):
    cursor.execute(comando_sql)
    colunas = [descricao[0] for descricao in cursor.description]
    linhas = cursor.fetchall()

    caminho_completo = os.path.join(PASTA_SAIDA, nome_arquivo)

    with open(caminho_completo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(colunas)
        escritor.writerows(linhas)

    print("Arquivo gerado:", nome_arquivo, "-", len(linhas), "linhas")


# ============================================================
# 1) Visao geral de orders (Questao 1)
# ============================================================
exportar_para_csv(
    "visao_geral_orders.csv",
    """
    SELECT
        COUNT(*) AS quantidade_linhas,
        strftime('%d/%m/%Y', MIN(created_at)) AS data_minima,
        strftime('%d/%m/%Y', MAX(created_at)) AS data_maxima,
        CAST(MIN(total) AS INTEGER) AS valor_minimo,
        CAST(MAX(total) AS INTEGER) AS valor_maximo,
        CAST(AVG(total) AS INTEGER) AS valor_medio
    FROM orders;
    """
)

# ============================================================
# 2) Clientes fieis - Top 10 (Questao 4)
# ============================================================
exportar_para_csv(
    "clientes_fieis_top10.csv",
    """
    WITH metricas AS (
        SELECT
            customer_id,
            SUM(total) AS faturamento_total,
            COUNT(id) AS frequencia,
            SUM(total) * 1.0 / COUNT(id) AS ticket_medio
        FROM orders
        WHERE total IS NOT NULL
        GROUP BY customer_id
    ),
    categorias AS (
        SELECT
            o.customer_id,
            COUNT(DISTINCT p.category_id) AS diversidade_categorias
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        JOIN product_variants pv ON pv.id = oi.product_variant_id
        JOIN products p ON p.id = pv.product_id
        GROUP BY o.customer_id
    )
    SELECT
        m.customer_id,
        CAST(m.faturamento_total AS INTEGER) AS faturamento_total,
        m.frequencia,
        CAST(m.ticket_medio AS INTEGER) AS ticket_medio,
        c.diversidade_categorias
    FROM metricas m
    JOIN categorias c ON c.customer_id = m.customer_id
    WHERE c.diversidade_categorias >= 13
    ORDER BY m.ticket_medio DESC, m.customer_id ASC
    LIMIT 10;
    """
)

# ============================================================
# 3) Vendas por dia da semana - lojas fisicas (Questao 5)
# ============================================================
exportar_para_csv(
    "vendas_dia_semana.csv",
    """
    WITH RECURSIVE datas(data) AS (
        SELECT MIN(date(created_at)) FROM orders WHERE channel = 'pos'
        UNION ALL
        SELECT date(data, '+1 day') FROM datas
        WHERE data < (SELECT MAX(date(created_at)) FROM orders WHERE channel = 'pos')
    ),
    calendario AS (
        SELECT
            data,
            CASE strftime('%w', data)
                WHEN '0' THEN 'Domingo'
                WHEN '1' THEN 'Segunda-feira'
                WHEN '2' THEN 'Terca-feira'
                WHEN '3' THEN 'Quarta-feira'
                WHEN '4' THEN 'Quinta-feira'
                WHEN '5' THEN 'Sexta-feira'
                WHEN '6' THEN 'Sabado'
            END AS dia_semana
        FROM datas
    ),
    vendas AS (
        SELECT date(created_at) AS data, SUM(total) AS valor_venda
        FROM orders
        WHERE channel = 'pos'
        GROUP BY date(created_at)
    )
    SELECT
        c.dia_semana,
        CAST(AVG(COALESCE(v.valor_venda, 0)) AS INTEGER) AS media_vendas
    FROM calendario c
    LEFT JOIN vendas v ON v.data = c.data
    GROUP BY c.dia_semana;
    """
)

# ============================================================
# 4) Produtos com nomes iguais e IDs diferentes
# ============================================================
exportar_para_csv(
    "produtos_nomes_duplicados.csv",
    """
    SELECT name AS nome_produto, id AS id_produto
    FROM products
    WHERE name IN (
        SELECT name FROM products GROUP BY name HAVING COUNT(*) > 1
    )
    ORDER BY name, id;
    """
)

conn.close()
print("")
print("Exportacao concluida. Arquivos salvos em:", PASTA_SAIDA)




# =================================================================================

# ============================================================
# Script completo: calcula a previsao da "Bussola de Bordo 702"
# e gera o CSV final para o Power BI, com cabecalho corrigido
# e separador compativel com o Excel brasileiro (;)
# ============================================================
import csv
import os
from datetime import datetime

# ------------------------------------------------------------
# PASSO 1: Caminhos dos arquivos de entrada e saida
# ------------------------------------------------------------
DIR_CSV = r"C:\Users\Wpere\Downloads\meu_projeto\csv"

ARQ_PRODUCTS = os.path.join(DIR_CSV, "products.csv")
ARQ_VARIANTS = os.path.join(DIR_CSV, "product_variants.csv")
ARQ_ORDERS = os.path.join(DIR_CSV, "orders.csv")
ARQ_ORDER_ITEMS = os.path.join(DIR_CSV, "order_items.csv")

CAMINHO_SAIDA = r"C:\Users\Wpere\Downloads\meu_projeto\power_bi_export\previsao_bussola.csv"
os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)


# ------------------------------------------------------------
# PASSO 2: Funcao simples para ler qualquer CSV
# ------------------------------------------------------------
def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


products = ler_csv(ARQ_PRODUCTS)
product_variants = ler_csv(ARQ_VARIANTS)
orders = ler_csv(ARQ_ORDERS)
order_items = ler_csv(ARQ_ORDER_ITEMS)


# ------------------------------------------------------------
# PASSO 3: Encontrar os IDs do produto "Bussola de Bordo 702"
# (busca sem depender de maiusculas/minusculas ou espacos)
# ------------------------------------------------------------
NOME_ALVO = "Bússola de Bordo 702"

ids_alvo = []
for produto in products:
    nome = produto["name"].strip().lower()
    if nome == NOME_ALVO.strip().lower():
        ids_alvo.append(produto["id"])

print("IDs encontrados para", NOME_ALVO, ":", ids_alvo)


# ------------------------------------------------------------
# PASSO 4: Mapear cada variante ao seu product_id
# ------------------------------------------------------------
variante_para_produto = {}
for variante in product_variants:
    if variante["product_id"] in ids_alvo:
        variante_para_produto[variante["id"]] = variante["product_id"]


# ------------------------------------------------------------
# PASSO 5: Guardar a data de cada pedido (order_id -> ano, mes)
# ------------------------------------------------------------
pedido_data = {}
for pedido in orders:
    try:
        dt = datetime.strptime(pedido["created_at"][:10], "%Y-%m-%d")
        pedido_data[pedido["id"]] = (dt.year, dt.month)
    except (KeyError, ValueError):
        continue


# ------------------------------------------------------------
# PASSO 6: Somar a quantidade vendida por mes
# - quant_comb: soma dos dois IDs juntos
# - quant_sep: cada ID tratado separadamente
# ------------------------------------------------------------
quant_comb = {}
quant_sep = {pid: {} for pid in ids_alvo}

for item in order_items:
    id_variante = item.get("product_variant_id") or item.get("variant_id")
    id_produto = variante_para_produto.get(id_variante)

    if id_produto is None:
        continue

    id_pedido = item["order_id"]
    mes = pedido_data.get(id_pedido)

    if mes is None:
        continue

    quantidade = int(item["quantity"])

    # cenario combinado
    if mes not in quant_comb:
        quant_comb[mes] = 0
    quant_comb[mes] += quantidade

    # cenario separado
    if mes not in quant_sep[id_produto]:
        quant_sep[id_produto][mes] = 0
    quant_sep[id_produto][mes] += quantidade


# ------------------------------------------------------------
# PASSO 7: Completar a serie mensal ate marco/2026 (preenche com 0)
# ------------------------------------------------------------
def completar_serie(dicionario, ano_fim=2026, mes_fim=3):
    if not dicionario:
        return {}

    ano, mes = min(dicionario.keys())
    serie = {}

    while (ano, mes) <= (ano_fim, mes_fim):
        serie[(ano, mes)] = dicionario.get((ano, mes), 0)
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1

    return serie


serie_comb = completar_serie(quant_comb)
serie_sep = {pid: completar_serie(quant_sep[pid]) for pid in ids_alvo}


# ------------------------------------------------------------
# PASSO 8: Calcular a previsao (media movel de 3 meses)
# ------------------------------------------------------------
def calcular_previsao(serie):
    meses_ordenados = sorted(serie.keys())
    previsao = {}

    for i in range(3, len(meses_ordenados)):
        mes_atual = meses_ordenados[i]
        tres_anteriores = meses_ordenados[i - 3:i]
        soma = sum(serie[m] for m in tres_anteriores)
        previsao[mes_atual] = round(soma / 3)

    return previsao


prev_comb = calcular_previsao(serie_comb)
prev_sep = {pid: calcular_previsao(serie_sep[pid]) for pid in ids_alvo}


# ------------------------------------------------------------
# PASSO 9: Calcular o MAE (erro medio absoluto) do 1o trimestre/2026
# ------------------------------------------------------------
meses_teste = [(2026, 1), (2026, 2), (2026, 3)]


def calcular_mae(serie, previsao):
    soma_erro = 0
    for mes in meses_teste:
        soma_erro += abs(serie.get(mes, 0) - previsao.get(mes, 0))
    return round(soma_erro / len(meses_teste))


mae_comb = calcular_mae(serie_comb, prev_comb)
mae_sep = {pid: calcular_mae(serie_sep[pid], prev_sep[pid]) for pid in ids_alvo}


# ------------------------------------------------------------
# PASSO 10 (AJUSTADO): Gravar o CSV final
# - encoding "utf-8-sig" evita que o Excel "quebre" o cabecalho
# - delimiter ";" garante que o Excel brasileiro separe as colunas
# - lineterminator "\n" evita linhas em branco entre os registros
# - todos os valores numericos sao convertidos para int
# ------------------------------------------------------------
with open(
    CAMINHO_SAIDA,
    "w",
    newline="",
    encoding="utf-8-sig"
) as arquivo:

    escritor = csv.writer(
        arquivo,
        delimiter=";",
        lineterminator="\n"
    )

    # cabecalho das colunas
    escritor.writerow([
        "mes",
        "vendido_real",
        "previsao",
        "mae",
        "cenario",
        "produto_id"
    ])

    # ---------------- linhas do cenario COMBINADO ----------------
    for mes in meses_teste:
        mes_formatado = "01/" + str(mes[1]).zfill(2) + "/" + str(mes[0])
        escritor.writerow([
            mes_formatado,
            int(serie_comb.get(mes, 0)),
            int(prev_comb.get(mes, 0)),
            int(mae_comb),
            "Combinado",
            "74 + 240"
        ])

    # ---------------- linhas do cenario SEPARADO ----------------
    for pid in ids_alvo:
        for mes in meses_teste:
            mes_formatado = "01/" + str(mes[1]).zfill(2) + "/" + str(mes[0])
            escritor.writerow([
                mes_formatado,
                int(serie_sep[pid].get(mes, 0)),
                int(prev_sep[pid].get(mes, 0)),
                int(mae_sep[pid]),
                "Separado",
                pid
            ])

print("")
print("Arquivo gerado com sucesso em:", CAMINHO_SAIDA)
print("")
print("Resumo COMBINADO:")
for mes in meses_teste:
    print(" ", mes, "-> real:", serie_comb.get(mes, 0), "| previsao:", prev_comb.get(mes, 0))
print("  MAE combinado:", mae_comb)

for pid in ids_alvo:
    print("")
    print("Resumo SEPARADO - ID", pid)
    for mes in meses_teste:
        print(" ", mes, "-> real:", serie_sep[pid].get(mes, 0), "| previsao:", prev_sep[pid].get(mes, 0))
    print("  MAE ID", pid, ":", mae_sep[pid])



    #=============================================================================================
    # Geracao do arquivo vendas_dia_semana.csv para o Power BI com ordenacao de dias da semana
    #=============================================================================================

    # ============================================================
# Script para gerar o CSV de vendas por dia da semana
# ja com a coluna ordem_dia, pronta para ordenacao no Power BI
# Delimitador: vírgula (mesmo padrao do arquivo ja importado)
# ============================================================
import csv
import os
import sqlite3

# ------------------------------------------------------------
# PASSO 1: Caminho do banco e do arquivo de saida
# ------------------------------------------------------------
CAMINHO_BANCO = "nautical.db"
CAMINHO_SAIDA = r"C:\Users\Wpere\Downloads\meu_projeto\power_bi_export\vendas_dia_semana.csv"

os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)

conn = sqlite3.connect(CAMINHO_BANCO)
cursor = conn.cursor()


# ------------------------------------------------------------
# PASSO 2: Consulta com o calendario, as vendas e a ordem dos dias
# ------------------------------------------------------------
cursor.execute(
    """
    WITH RECURSIVE datas(data) AS (
        SELECT MIN(date(created_at)) FROM orders WHERE channel = 'pos'
        UNION ALL
        SELECT date(data, '+1 day') FROM datas
        WHERE data < (SELECT MAX(date(created_at)) FROM orders WHERE channel = 'pos')
    ),
    calendario AS (
        SELECT
            data,

            -- Nome do dia em portugues
            CASE strftime('%w', data)
                WHEN '1' THEN 'Segunda-feira'
                WHEN '2' THEN 'Terça-feira'
                WHEN '3' THEN 'Quarta-feira'
                WHEN '4' THEN 'Quinta-feira'
                WHEN '5' THEN 'Sexta-feira'
                WHEN '6' THEN 'Sábado'
                WHEN '0' THEN 'Domingo'
            END AS dia_semana,

            -- Numero da ordem, comecando na segunda-feira (1) ate domingo (7)
            CASE strftime('%w', data)
                WHEN '1' THEN 1
                WHEN '2' THEN 2
                WHEN '3' THEN 3
                WHEN '4' THEN 4
                WHEN '5' THEN 5
                WHEN '6' THEN 6
                WHEN '0' THEN 7
            END AS ordem_dia

        FROM datas
    ),
    vendas AS (
        SELECT
            date(created_at) AS data,
            SUM(total) AS valor_venda
        FROM orders
        WHERE channel = 'pos'
        GROUP BY date(created_at)
    )
    SELECT
        c.dia_semana,
        CAST(AVG(COALESCE(v.valor_venda, 0)) AS INTEGER) AS media_vendas,
        c.ordem_dia
    FROM calendario c
    LEFT JOIN vendas v ON v.data = c.data
    GROUP BY c.dia_semana, c.ordem_dia

    -- Ja ordena o resultado antes mesmo de gravar no CSV
    ORDER BY c.ordem_dia;
    """
)

linhas = cursor.fetchall()
conn.close()


# ------------------------------------------------------------
# PASSO 3: Gravar o CSV com vírgula e cabecalho garantido
# ------------------------------------------------------------
with open(
    CAMINHO_SAIDA,
    "w",
    newline="",
    encoding="utf-8-sig"
) as arquivo:

    escritor = csv.writer(
        arquivo,
        delimiter=",",
        lineterminator="\n"
    )

    # Cabecalho das colunas
    escritor.writerow(["dia_semana", "media_vendas", "ordem_dia"])

    # Linhas ja na ordem correta (segunda a domingo)
    for dia_semana, media_vendas, ordem_dia in linhas:
        escritor.writerow([dia_semana, int(media_vendas), int(ordem_dia)])

print("Arquivo gerado com sucesso:", CAMINHO_SAIDA)
print("")
print("Ordem gravada no arquivo:")
for dia_semana, media_vendas, ordem_dia in linhas:
    print(ordem_dia, "-", dia_semana, "-> media:", media_vendas)