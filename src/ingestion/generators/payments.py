import pandas as pd
import random
from loguru import logger
from datetime import datetime, timedelta

METHODS      = ["credit_card", "pix", "boleto"]
METHOD_W     = [55, 35, 10]
STATUSES     = ["approved", "refused", "chargeback"]
STATUS_W     = [89, 8, 3]

def generate_payments(orders_df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """
    Gera pagamentos para cada pedido da DataCommerce.
    """
    logger.info(f"Gerando pagamentos para {len(orders_df)} pedidos...")
    random.seed(seed)
    
    payments = []
    for i, (_, row) in enumerate(orders_df.iterrows(), start=1):
        method = random.choices(METHODS, weights=METHOD_W)[0]
        status = random.choices(STATUSES, weights=STATUS_W)[0]
        
        if method == "credit_card":
            installments = random.choices(
                [1, 2, 3, 6, 12],
                weights=[40, 15, 15, 15, 15]
            )[0]
        else:
            installments = 1
        
        order_date: pd.Timestamp = pd.to_datetime(str(row["order_date"]))
        processed_at = order_date + timedelta(minutes=random.randint(1, 180))
        
        payments.append({
            "payment_id":     f"PAY-{i:06d}",
            "order_id":       row["order_id"],
            "method":         method,
            "status":         status,
            "amount":         row["total_amount"],
            "installments":   installments,
            "processed_at":   processed_at.isoformat(),
            "ingestion_at":   datetime.utcnow().isoformat(),
        })
    
    df = pd.DataFrame(payments)
    logger.success(
        f"{len(df)} pagamentos gerados | "
        f"Aprovados: {(df['status']=='approved').sum()} | "
        f"Recusados: {(df['status']=='refused').sum()} | "
        f"Chargebacks: {(df['status']=='chargeback').sum()}"
    )
    return df