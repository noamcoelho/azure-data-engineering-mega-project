import pandas as pd
import random
from loguru import logger
from datetime import datetime, timedelta

STATUSES    = ["pending", "confirmed", "shipped", "delivered", "cancelled", "returned"]
STATUS_W    = [5, 20, 15, 50, 7, 3]
CHANNELS    = ["website", "app", "marketplace"]

def generate_orders(
    n:            int,
    customer_ids: list,
    product_ids:  list,
    seed:         int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Gera pedidos e itens de pedido da DataCommerce.
    
    Returns:
        Tupla (orders_df, order_items_df)
    """
    logger.info(f"Gerando {n} pedidos...")
    random.seed(seed)
    
    orders      = []
    order_items = []
    
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(1, n + 1):
        order_date    = start_date + timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        num_items     = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
        items_list    = []
        
        for j in range(num_items):
            product_id = random.choice(product_ids)
            quantity   = random.randint(1, 3)
            unit_price = round(random.uniform(20, 1500), 2)
            discount   = round(random.uniform(0, 0.30), 2) if random.random() > 0.7 else 0
            
            items_list.append({
                "order_item_id": f"ITEM-{i:06d}-{j+1:02d}",
                "order_id":      f"ORD-{i:06d}",
                "product_id":    product_id,
                "quantity":      quantity,
                "unit_price":    unit_price,
                "discount_pct":  discount,
                "subtotal":      round(unit_price * quantity * (1 - discount), 2),
            })
        
        total_amount  = sum(item["subtotal"] for item in items_list)
        freight       = round(random.uniform(0, 35), 2)
        
        orders.append({
            "order_id":      f"ORD-{i:06d}",
            "customer_id":   random.choice(customer_ids),
            "order_date":    order_date.isoformat(),
            "status":        random.choices(STATUSES, weights=STATUS_W)[0],
            "channel":       random.choice(CHANNELS),
            "total_amount":  round(total_amount + freight, 2),
            "freight":       freight,
            "num_items":     num_items,
            # Dados intencionalmente sujos
            "coupon_code":   f"DESC{random.randint(10,30)}" if random.random() > 0.8 else None,
            "ingestion_at":  datetime.utcnow().isoformat(),
        })
        order_items.extend(items_list)
    
    orders_df = pd.DataFrame(orders)
    items_df  = pd.DataFrame(order_items)
    
    logger.success(
        f"{len(orders_df)} pedidos gerados | "
        f"Total de itens: {len(items_df)} | "
        f"Receita total: R$ {orders_df['total_amount'].sum():,.2f}"
    )
    return orders_df, items_df