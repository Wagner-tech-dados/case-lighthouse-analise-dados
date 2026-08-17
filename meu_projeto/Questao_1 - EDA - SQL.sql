---------------------------------------------------------------------------------------------
-- QUESTAO 1 - EDA --
---------------------------------------------------------------------------------------------
-- Legenda [P1] - Parte 1 / [P2] Parte 2
SELECT * FROM orders o 

-- Consulta exercício 1 sem formatacao de data
SELECT
COUNT(*) AS quantidade_linhas
FROM orders;

-- Consulta exercicio 1 com formatacao de data e valores, Consulta FULL
SELECT
-- [P1] Consulta quantidade de linhas com formatacao para dd/mm/aaaa    
	COUNT(*) AS quantidade_linhas,
    strftime('%d/%m/%Y', MIN(created_at)) AS data_minima,
    strftime('%d/%m/%Y', MAX(created_at)) AS data_maxima,
 -- [P2], valor minimo, maximo e medio com concatenacao de R$
    'R$ ' || MIN(total) AS valor_minimo,
    'R$ ' || MAX(total) AS valor_maximo,
    'R$ ' || ROUND(AVG(total),2) AS valor_medio
FROM orders;

-- [P1] Subconsulta com quantidade de colunas
SELECT COUNT(*) AS quantidade_colunas
FROM pragma_table_info('orders');

---------------------------------------------------------------------------------------------
-- [CONFERENCIAS] -- 
---------------------------------------------------------------------------------------------

-- Conferencia quantidade de linhas
SELECT
    COUNT(*) AS total_linhas,
    COUNT(total) AS total_total_preenchido,
    COUNT(*) - COUNT(total) AS total_total_nulo
FROM orders;

-- Conferencia para identificar valores zerados ou negativos
SELECT
    COUNT(*) FILTER (WHERE total = 0) AS total_zero,
    COUNT(*) FILTER (WHERE total < 0) AS total_negativo
FROM orders;

-- Conferencia para identificar duplicidades na coluna id, caso negativo, a consulta nao trara nenhuma informacao
SELECT
    id,
    COUNT(*) AS quantidade
FROM orders
GROUP BY id
HAVING COUNT(*) > 1;
-- [FIM DAS CONFERENCIAS] -- 

---------------------------------------------------------------------------------------------
-- [OUTLIER] --
---------------------------------------------------------------------------------------------

-- Limites superiores
SELECT total
FROM orders
WHERE total IS NOT NULL
ORDER BY total DESC
LIMIT 20;

-- Limites inferiores
SELECT total
FROM orders
WHERE total IS NOT NULL
ORDER BY total ASC
LIMIT 20;

---------------------------------------------------------------------------------------------
-- [FIM OUTLIER] -- 
---------------------------------------------------------------------------------------------


-- Consulta se existem valores nulos
SELECT
    COUNT(*) AS total_linhas,
    COUNT(total) AS total_preenchidos,
    COUNT(*) - COUNT(total) AS total_nulos
FROM orders;

---------------------------------------------------------------------------------------------
-- QUESTAO 1.1 - SQL
-- Codigo Calculo
---------------------------------------------------------------------------------------------

-- Quantidade total de linhas
SELECT COUNT(*) AS quantidade_linhas
FROM orders;

-- Intervalo de datas analisado (data minima e maxima

SELECT
-- [Questao 1.1] Consulta quantidade de linhas com formatacao para dd/mm/aaaa, minimo e maximo   
    strftime('%d/%m/%Y', MIN(created_at)) AS data_minima,
    strftime('%d/%m/%Y', MAX(created_at)) AS data_maxima
FROM orders;

-- [Questao 1.1] Consulta valor minimo com concatenacao de R$
SELECT
    'R$ ' || MIN(total) AS valor_minimo
 FROM orders;

SELECT
 -- [Questao 1.1] Consulta Valor maximo com concatenacao de R$
    'R$ ' || MAX(total) AS valor_maximo
FROM orders;

SELECT
 -- [Questao 1.1] Consulta Valor medio com concatenacao de R$
    'R$ ' || ROUND(AVG(total),2) AS valor_medio
FROM orders;

---------------------------------------------------------------------------------------------
-- Questao 4 - Analise de Clientes
---------------------------------------------------------------------------------------------
-- Cenário 
-- A Diretoria da LH Nautical deseja identificar os clientes fieis. Diferente de quem compra muito uma única vez, o cliente fiel é o cliente que possui um gasto médio alto por transação e navega por diversas categorias da loja. 
-- O objetivo é mapear o que esses clientes de elite estão consumindo para replicar o comportamento em outros segmentos.

---------------------------------------------------------------------------------------------
--Premissas obrigatórias: 
---------------------------------------------------------------------------------------------
-- Faturamento Total: Soma da coluna total por cliente. 
-- Frequência: Contagem total de transações (IDs de venda) por cliente. 
-- Ticket Médio: Faturamento Total / Frequência. 
-- Diversidade de Categorias: Quantidade de categorias distintas (category_id) que o cliente comprou. 
-- Filtro de Elite: Apenas clientes que compraram produtos de 13 ou mais categorias distintas devem ser considerados no ranking. 
-- Desempate: Em caso de empate no Ticket Médio, utilize o customer_id em ordem crescente. 
 
---------------------------------------------------------------------------------------------
-- Tarefa: 
---------------------------------------------------------------------------------------------
-- Calcule o Ticket Médio e a Diversidade de Categorias para cada customer_id. 
-- Filtre os 10 clientes com o maior Ticket Médio que atendam ao critério de diversidade (13 ou + categorias). 
-- Para este grupo específico de 10 clientes, identifique qual categoria de produto concentra a maior quantidade total de itens comprados (sum(quantity)). 

---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------


---------------------------------------------------------------------------------------------
-- Cria uma tabela temporaria com os cálculos financeiros de cada cliente
---------------------------------------------------------------------------------------------
CREATE TEMP TABLE metricas_cliente AS
SELECT
    customer_id,

    -- Soma tudo que o cliente gastou
    SUM(total) AS faturamento_total,

    -- Conta quantos pedidos (transações) o cliente fez
    COUNT(id) AS frequencia,

    -- Ticket médio = faturamento dividido pela quantidade de pedidos
    -- O "* 1.0" garante que o resultado tenha casas decimais
    SUM(total) * 1.0 / COUNT(id) AS ticket_medio

FROM orders
WHERE total IS NOT NULL
GROUP BY customer_id;

SELECT * FROM metricas_cliente


CREATE TEMP TABLE categorias_cliente AS
SELECT
    o.customer_id,

    -- Conta as categorias diferentes, sem repetir
    COUNT(DISTINCT p.category_id) AS diversidade_categorias

FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.id
JOIN product_variants AS pv ON pv.id = oi.product_variant_id
JOIN products AS p ON p.id = pv.product_id

GROUP BY o.customer_id;


SELECT * FROM categorias_cliente

---------------------------------------------------------------------------------------------
--  Juntar tudo, aplicar o filtro e pegar os 10 melhores
---------------------------------------------------------------------------------------------
CREATE TEMP TABLE clientes_elite AS
SELECT
    m.customer_id,
    m.faturamento_total,
    m.frequencia,
    m.ticket_medio,
    c.diversidade_categorias

FROM metricas_cliente AS m
JOIN categorias_cliente AS c ON c.customer_id = m.customer_id

-- Regra de elite: só entram clientes com 13 categorias ou mais
WHERE c.diversidade_categorias >= 13

---------------------------------------------------------------------------------------------
-- Ordena do maior ticket médio para o menor
---------------------------------------------------------------------------------------------
-- Em caso de empate, o cliente com menor customer_id vem primeiro
---------------------------------------------------------------------------------------------
ORDER BY
    m.ticket_medio DESC,
    m.customer_id ASC

-- Pega apenas os 10 primeiros
LIMIT 10;

---------------------------------------------------------------------------------------------
--  Ver o ranking final dos 10 clientes
---------------------------------------------------------------------------------------------
SELECT
    customer_id,
    ROUND(faturamento_total, 2) AS faturamento_total,
    frequencia,
    ROUND(ticket_medio, 2) AS ticket_medio,
    diversidade_categorias
FROM clientes_elite
ORDER BY ticket_medio DESC;

---------------------------------------------------------------------------------------------
-- Descobrir a categoria mais comprada por esses 10 clientes
---------------------------------------------------------------------------------------------
SELECT
    c.name AS categoria,
    SUM(oi.quantity) AS total_itens_comprados

FROM order_items AS oi
JOIN orders AS o ON o.id = oi.order_id
JOIN product_variants AS pv ON pv.id = oi.product_variant_id
JOIN products AS p ON p.id = pv.product_id
JOIN categories AS c ON c.id = p.category_id

---------------------------------------------------------------------------------------------
-- Filtra somente os pedidos feitos pelos 10 clientes de elite
---------------------------------------------------------------------------------------------
WHERE o.customer_id IN (SELECT customer_id FROM clientes_elite)
GROUP BY c.name
ORDER BY total_itens_comprados DESC
LIMIT 1;



---------------------------------------------------------------------------------------------
-- QUESTÃO 5.1
-- DIMENSÃO DE CALENDÁRIO CRUZADA COM VENDAS (LOJAS FÍSICAS)
---------------------------------------------------------------------------------------------

-- Cria um calendário com todos os dias entre a primeira e a última
-- venda registrada em lojas físicas (channel = 'pos')

---------------------------------------------------------------------------------------------
-- Consultas independentes
---------------------------------------------------------------------------------------------

WITH RECURSIVE limites AS (
    -- Calcula a data mínima e máxima UMA ÚNICA VEZ
    SELECT
        MIN(date(created_at)) AS data_min,
        MAX(date(created_at)) AS data_max
    FROM orders
    WHERE channel = 'pos'
),
datas(data) AS (
    -- Primeira linha: usa o limite já calculado
    SELECT data_min FROM limites

    UNION ALL

    -- Cada nova linha soma 1 dia, comparando com o limite já calculado
    SELECT date(data, '+1 day')
    FROM datas, limites
    WHERE data < limites.data_max
)
SELECT
    data,
    CASE strftime('%w', data)
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Segunda-feira'
        WHEN '2' THEN 'Terça-feira'
        WHEN '3' THEN 'Quarta-feira'
        WHEN '4' THEN 'Quinta-feira'
        WHEN '5' THEN 'Sexta-feira'
        WHEN '6' THEN 'Sábado'
    END AS dia_semana
FROM datas;

---------------------------------------------------------------------------------------------
-- Fim consultas independentes
---------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------
-- Consultas consolidadas
---------------------------------------------------------------------------------------------

CREATE TEMP TABLE calendario AS
WITH RECURSIVE datas(data) AS (

    -- Primeira linha: a data mais antiga de venda em loja física
    SELECT MIN(date(created_at))
    FROM orders
    WHERE channel = 'pos'
	

    UNION ALL

    -- Cada nova linha soma 1 dia à data anterior
    SELECT date(data, '+1 day')
    FROM datas
    WHERE data < (
        SELECT MAX(date(created_at))
        FROM orders
        WHERE channel = 'pos'
    )
)
SELECT
    data,

    -- Traduz o número do dia da semana (0 a 6) para português
    -- 0 = Domingo, 1 = Segunda ... 6 = Sábado
    CASE strftime('%w', data)
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Segunda-feira'
        WHEN '2' THEN 'Terça-feira'
        WHEN '3' THEN 'Quarta-feira'
        WHEN '4' THEN 'Quinta-feira'
        WHEN '5' THEN 'Sexta-feira'
        WHEN '6' THEN 'Sábado'
    END AS dia_semana

FROM datas;

---------------------------------------------------------------------------------------------
-- Cruzar o calendário com as vendas e calcular a média por dia da semana
---------------------------------------------------------------------------------------------
SELECT
    c.dia_semana,

    -- Média considerando TODOS os dias do calendário,
    -- inclusive os dias sem venda (tratados como 0)
    AVG(COALESCE(v.valor_venda, 0)) AS media_vendas

FROM calendario AS c

-- LEFT JOIN garante que todo dia do calendário apareça,
-- mesmo quando não existe venda naquele dia
LEFT JOIN (

    -- Soma o valor de venda de cada dia, somente lojas físicas
    SELECT
        date(created_at) AS data,
        SUM(total) AS valor_venda
    FROM orders
    WHERE channel = 'pos'
    GROUP BY date(created_at)

) AS v ON v.data = c.data

GROUP BY c.dia_semana


-- Ordena do pior para o melhor dia de vendas
ORDER BY media_vendas ASC;

---------------------------------------------------------------------------------------------
-- Fim do exercicio
---------------------------------------------------------------------------------------------

SELECT * FROM products
WHERE name ="asdf"


