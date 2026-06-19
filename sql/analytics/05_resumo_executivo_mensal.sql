-- Query: Resumo executivo mensal com variação percentual de receita
-- Pergunta de negócio: Como a receita evoluiu mês a mês? 
--                      Quais meses tiveram crescimento ou queda?
-- Camada: Analytics (Gold)
-- Autor: Noam Coelho

WITH receita_mensal AS (
    SELECT 
        STRFTIME('%Y-%m', order_date)   AS mes,
        SUM(total_amount)               AS receita_total,
        COUNT(*)                        AS total_pedidos,
        ROUND(AVG(total_amount), 2)     AS ticket_medio
    FROM orders
    WHERE status != 'cancelled'
    GROUP BY STRFTIME('%Y-%m', order_date)
),
resumo_com_variacao AS (
    SELECT 
        mes,
        receita_total,
        total_pedidos,
        ticket_medio,
        LAG(receita_total) OVER (ORDER BY mes)  AS receita_mes_anterior,
        ROUND(
            (receita_total - LAG(receita_total) OVER (ORDER BY mes)) 
            / LAG(receita_total) OVER (ORDER BY mes) * 100
        , 1)                                    AS variacao_pct
    FROM receita_mensal
)
SELECT 
    mes,
    receita_total,
    total_pedidos,
    ticket_medio,
    receita_mes_anterior,
    variacao_pct,
    CASE 
        WHEN variacao_pct > 0  THEN 'Alta'
        WHEN variacao_pct < 0  THEN 'Queda'
        WHEN variacao_pct = 0  THEN 'Estavel'
        ELSE 'Primeiro mes'
    END AS tendencia
FROM resumo_com_variacao
ORDER BY mes;