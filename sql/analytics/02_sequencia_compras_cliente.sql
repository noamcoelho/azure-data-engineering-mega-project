-- Query: Posição de cada pedido na sequência de compras do cliente
-- Pergunta de negócio: É o primeiro pedido do cliente? O segundo? 
--                      Usado para análise de recorrência e funil de retenção.
-- Camada: Analytics (Gold)
-- Autor: Noam Coelho

SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount,
    ROW_NUMBER() OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) AS posicao_compra
FROM orders o
ORDER BY o.customer_id, posicao_compra;