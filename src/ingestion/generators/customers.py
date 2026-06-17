import pandas as pd 
from faker import Faker
import random 
from loguru import logger
from datetime import datetime

fake = Faker("pt_BR")

def generate_customers(n: int = 1_000, seed: int = 42) -> pd.DataFrame:
    """
    Gera dataset sintético de clientes da DataCommerce.
    
    Args:
        n: número de clientes a gerar
        seed: seed para reprodutibilidade
        
    Returns:
        DataFrame com dados de clientes
    """
    logger.info(f"Gerando {n} clientes...")
    
    Faker.seed(seed)
    random.seed(seed)
    
    segments   = ["Bronze", "Silver", "Gold", "Platinum"]
    channels   = ["website", "app", "marketplace"]
    
    customers = []
    for i in range(1, n + 1):
        signup_date = fake.date_between(
            start_date="-3y", end_date="today"
        )
        customers.append({
            "customer_id":    f"CUST-{i:06d}",
            "name":           fake.name(),
            "email":          fake.email(),
            "phone":          fake.phone_number(),
            "cpf":            fake.cpf(),
            "birth_date":     fake.date_of_birth(
                                  minimum_age=18, maximum_age=75
                              ).isoformat(),
            "city":           fake.city(),
            "state":          fake.estado_sigla(),
            "country":        "Brasil",
            "segment":        random.choices(
                                  segments,
                                  weights=[50, 30, 15, 5]
                              )[0],
            "signup_date":    signup_date.isoformat(),
            "acquisition_channel": random.choice(channels),
            "is_active":      random.choices(
                                  [True, False],
                                  weights=[85, 15]
                              )[0],
            # Dados intencionalmente sujos para praticar qualidade
            "loyalty_score":  random.randint(0, 100) if random.random() > 0.05 else None,
            "ingestion_at":   datetime.utcnow().isoformat(),
        })
    
    df = pd.DataFrame(customers)
    logger.success(f"{len(df)} clientes gerados | "
                   f"Ativos: {df['is_active'].sum()} | "
                   f"Nulos em loyalty_score: {df['loyalty_score'].isna().sum()}")
    return df