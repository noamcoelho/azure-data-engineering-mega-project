-- Query: Clientes ativos que não compram há mais de 90 dias
-- Pergunta de negócio: Quais clientes estão em risco de churn e precisam 
--                      de ações de reativação (cupom, campanha, contato)?
-- Camada: Analytics (Gold)
-- Autor: Noam Coelho

WITH ultima_compra AS (
    SELECT 
        customer_id,
        MAX(order_date)     AS data_ultimo_pedido,
        COUNT(*)            AS total_pedidos
    FROM orders
    GROUP BY customer_id
),
data_referencia AS (
    SELECT MAX(order_date) AS data_max FROM orders
),
clientes_inativos AS (
    SELECT 
        u.customer_id,
        u.data_ultimo_pedido,
        u.total_pedidos,
        CAST(
            JULIANDAY((SELECT data_max FROM data_referencia)) - 
            JULIANDAY(u.data_ultimo_pedido) 
        AS INTEGER) AS dias_sem_compra
    FROM ultima_compra u
    WHERE CAST(
        JULIANDAY((SELECT data_max FROM data_referencia)) - 
        JULIANDAY(u.data_ultimo_pedido) 
    AS INTEGER) > 90
)
SELECT 
    c.customer_id,
    c.name,
    c.segment,
    c.email,
    ci.data_ultimo_pedido,
    ci.dias_sem_compra,
    ci.total_pedidos
FROM clientes_inativos ci
INNER JOIN customers c ON ci.customer_id = c.customer_id
WHERE c.is_active = 1
ORDER BY ci.dias_sem_compra DESC;