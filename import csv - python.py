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