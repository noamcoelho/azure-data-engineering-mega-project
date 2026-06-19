-- Query: Pedidos com valor acima de 3 desvios-padrão da média
-- Pergunta de negócio: Existem pedidos com valores anômalos que podem indicar 
--                      erro de precificação, fraude ou problema de dados?
-- Camada: Analytics (Gold) / Data Quality
-- Autor: Noam Coelho

WITH estatisticas AS (
    SELECT 
        AVG(total_amount)                                               AS media,
        AVG(total_amount * total_amount) - AVG(total_amount) * AVG(total_amount) AS variancia
    FROM orders
),
limites AS (
    SELECT 
        media,
        media + 3 * SQRT(variancia) AS limite_superior
    FROM estatisticas
)
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount,
    ROUND(l.media, 2)           AS media_geral,
    ROUND(l.limite_superior, 2) AS limite_3_desvios
FROM orders o, limites l
WHERE o.total_amount > l.limite_superior
ORDER BY o.total_amount DESC;