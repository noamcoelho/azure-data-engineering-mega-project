import pandas as pd
import random
import uuid
from loguru import logger
from datetime import datetime, timedelta

EVENT_TYPES   = ["page_view", "add_to_cart", "checkout_start", "purchase", "abandon_cart"]
EVENT_W       = [55, 20, 10, 8, 7]
DEVICES       = ["mobile", "desktop", "tablet"]
DEVICE_W      = [60, 32, 8]

def generate_events(
    n:            int,
    customer_ids: list,
    product_ids:  list,
    seed:         int = 42
) -> pd.DataFrame:
    """
    Gera eventos de navegação do site/app da DataCommerce.
    
    Args:
        n: número de eventos a gerar
        customer_ids: lista de IDs de clientes existentes
        product_ids: lista de IDs de produtos existentes
        seed: seed para reprodutibilidade
        
    Returns:
        DataFrame com eventos de navegação
    """
    logger.info(f"Gerando {n} eventos de navegação...")
    random.seed(seed)
    
    start_date = datetime.now() - timedelta(days=90)
    
    # Sessões: simulam visitantes navegando, alguns anônimos
    num_sessions = max(1, n // 4)
    sessions = [str(uuid.uuid4()) for _ in range(num_sessions)]
    
    events = []
    for i in range(1, n + 1):
        session_id  = random.choice(sessions)
        # 30% das sessões são anônimas (sem customer_id)
        is_anonymous = random.random() < 0.30
        customer_id  = None if is_anonymous else random.choice(customer_ids)
        
        event_type  = random.choices(EVENT_TYPES, weights=EVENT_W)[0]
        # page_view não precisa estar associado a um produto necessariamente
        product_id  = (
            random.choice(product_ids)
            if event_type != "page_view" or random.random() > 0.5
            else None
        )
        
        timestamp = start_date + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        events.append({
            "event_id":      f"EVT-{i:07d}",
            "session_id":    session_id,
            "customer_id":   customer_id,
            "event_type":    event_type,
            "product_id":    product_id,
            "timestamp":     timestamp.isoformat(),
            "device":        random.choices(DEVICES, weights=DEVICE_W)[0],
            "ingestion_at":  datetime.utcnow().isoformat(),
        })
    
    df = pd.DataFrame(events)
    pct_anon = df["customer_id"].isna().mean() * 100
    logger.success(
        f"{len(df)} eventos gerados | "
        f"Sessões únicas: {df['session_id'].nunique()} | "
        f"Anônimos: {pct_anon:.1f}%"
    )
    return df