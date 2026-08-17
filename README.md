# Case de Análise de Vendas Náuticas

Projeto de análise de dados desenvolvido com **SQLite, Python, SQL e Power BI**, com o objetivo de transformar dados de pedidos em informações úteis para acompanhamento de vendas, comportamento dos clientes e previsão de demanda.

## Objetivo do projeto

Este case foi desenvolvido para demonstrar as etapas de um projeto de dados:

- Organização e preparação dos dados;
- Criação e consulta de um banco SQLite;
- Tratamento dos dados utilizando SQL e Python;
- Análise de vendas por período e dia da semana;
- Identificação de clientes e produtos;
- Tratamento de produtos com nomes iguais e IDs diferentes;
- Criação de previsões de vendas;
- Desenvolvimento de um dashboard no Power BI.

## Tecnologias utilizadas

- **Python**
- **SQLite**
- **SQL**
- **Power BI**
- **CSV**
- **Git e GitHub**

## Estrutura do projeto

```text
.
├── meu_projeto/
│   ├── csv/
│   ├── power_bi_export/
│   ├── scripts/
│   └── ...
├── codigos python.py
├── import csv - python.py
├── schema_gerado_python-sql.sql
├── .gitignore
└── README.md
```

## Fluxo da análise

```text
Dados brutos
     ↓
Tratamento com Python e SQL
     ↓
Banco de dados SQLite
     ↓
Exportação para arquivos CSV
     ↓
Importação no Power BI
     ↓
Dashboard e análise dos resultados
```

## Principais etapas

### 1. Criação do banco de dados

O arquivo `schema_gerado_python-sql.sql` contém a estrutura utilizada para criação e organização das tabelas no banco SQLite.

Nessa etapa foram definidos:

- Tabelas;
- Campos;
- Tipos de dados;
- Relacionamentos;
- Comandos de tratamento dos dados.

### 2. Tratamento dos dados

Os scripts em Python e SQL foram utilizados para:

- Importar arquivos CSV;
- Criar e consultar o banco SQLite;
- Corrigir tipos de dados;
- Organizar informações de pedidos;
- Gerar arquivos para o Power BI;
- Preparar os dados para análise.

### 3. Tabela de datas

Foi criada uma tabela calendário para garantir que todos os dias do período fossem considerados, inclusive os dias sem vendas.

Essa tabela permite:

- Analisar vendas por dia, mês e ano;
- Organizar os dias da semana na ordem correta;
- Considerar dias sem vendas no cálculo das médias;
- Evitar resultados distorcidos na análise.

Os dias da semana foram organizados na seguinte sequência:

1. Segunda-feira;
2. Terça-feira;
3. Quarta-feira;
4. Quinta-feira;
5. Sexta-feira;
6. Sábado;
7. Domingo.

### 4. Tratamento de produtos

Produtos com o mesmo nome, mas com IDs diferentes, foram mantidos como itens distintos.

Essa decisão evita a união indevida de produtos diferentes e preserva a identificação original dos registros.

Também foi identificada a ocorrência do produto `asdf`, classificado como possível inconsistência cadastral para validação posterior.

### 5. Previsão de vendas

A análise também apresenta uma comparação entre vendas reais e valores previstos para o primeiro trimestre de 2026.

Indicadores utilizados:

- Vendas reais;
- Previsão mensal;
- Previsão total;
- MAE, que representa o erro médio da previsão.

## Principais indicadores

| Indicador | Resultado |
|---|---:|
| Total de pedidos | 48.998 |
| Valor médio dos pedidos | R$ 28.704 |
| Previsão total do 1º trimestre de 2026 | 149 unidades |
| MAE da previsão | 19 |

## Dashboard

O dashboard foi desenvolvido no Power BI e apresenta:

- Total de pedidos;
- Valor médio dos pedidos;
- Vendas médias por dia da semana;
- Ticket médio dos clientes fiéis;
- Produtos com nomes iguais e IDs diferentes;
- Comparação entre vendas reais e previsão;
- Previsão total para o primeiro trimestre de 2026;
- Indicador de erro médio da previsão.

### Visualização do dashboard

Adicione uma imagem do dashboard nesta seção:

```markdown
![Dashboard do projeto](meu_projeto/imagens/dashboard.png)
```

Para que a imagem apareça no GitHub, salve o arquivo, por exemplo, em:

```text
meu_projeto/imagens/dashboard.png
```

## Como executar o projeto

### Pré-requisitos

É necessário ter instalado:

- Python 3;
- SQLite;
- Power BI Desktop, caso queira visualizar o dashboard.

### 1. Clonar o repositório

```bash
git clone LINK_DO_SEU_REPOSITORIO
```

### 2. Acessar a pasta do projeto

```bash
cd NOME_DO_REPOSITORIO
```

### 3. Executar os scripts

Os scripts Python podem ser executados pelo terminal:

```bash
python "codigos python.py"
```

ou:

```bash
python "import csv - python.py"
```

Os arquivos CSV gerados devem ser salvos na pasta de exportação definida no projeto.

### 4. Abrir o dashboard

Depois de gerar os arquivos CSV:

1. Abra o Power BI Desktop;
2. Atualize as fontes de dados;
3. Confirme os tipos das colunas;
4. Verifique a ordenação dos dias da semana;
5. Atualize os visuais do dashboard.

## Cuidados importantes

- Os arquivos CSV devem utilizar o delimitador definido no projeto;
- As colunas de valores devem estar configuradas como números;
- As colunas de data devem utilizar o formato `dd/mm/aaaa`;
- A coluna `ordem_dia` deve ser utilizada para ordenar `dia_semana`;
- Produtos com IDs diferentes não devem ser agrupados apenas pelo nome;
- O cenário `Combinado` deve ser utilizado nos visuais de previsão quando essa for a regra da análise.

## Resultados e aprendizados

O projeto demonstrou a importância de:

- Utilizar uma tabela calendário em análises temporais;
- Considerar dias sem vendas nos cálculos de média;
- Separar produtos pelo ID, mesmo quando possuem o mesmo nome;
- Validar as agregações utilizadas no Power BI;
- Comparar valores reais e previstos;
- Documentar as decisões tomadas durante o tratamento dos dados.

## Possíveis melhorias

Como próximos passos, podem ser adicionados:

- Automatização completa da atualização dos arquivos;
- Novos indicadores de margem e rentabilidade;
- Análise por canal de venda;
- Segmentação de clientes;
- Monitoramento de produtos com inconsistências cadastrais;
- Novos modelos de previsão;
- Publicação de uma versão interativa do dashboard.

## Observação sobre os dados

Este projeto foi disponibilizado para fins educacionais e de demonstração. Os dados utilizados não devem conter informações pessoais ou confidenciais.

## Autor

**Wagner Tech Dados**

Projeto desenvolvido para demonstrar conhecimentos em análise de dados, SQL, Python, SQLite e Power BI.
