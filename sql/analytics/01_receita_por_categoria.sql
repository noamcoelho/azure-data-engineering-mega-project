-- Query: Receita total por categoria de produto
-- Pergunta de negócio: Quais categorias geram mais receita para a DataCommerce?
-- Camada: Analytics (Gold)
-- Autor: Noam Coelho

SELECT 
    p.category,
    SUM(oi.subtotal)                    AS receita_total,
    COUNT(DISTINCT oi.order_id)         AS total_pedidos,
    ROUND(AVG(oi.subtotal), 2)          AS ticket_medio_item
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY receita_total DESC;