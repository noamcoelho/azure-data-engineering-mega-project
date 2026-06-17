import pandas as pd 
from faker import Faker
import random 
from loguru import logger
from datetime import datetime

fake = Faker("pt_BR")

CATEGORIES = {
    "Eletrônicos":    ["Smartphone", "Notebook", "Tablet", "Fone de Ouvido", "Smartwatch"],
    "Moda":           ["Camiseta", "Calça Jeans", "Vestido", "Tênis", "Bolsa"],
    "Casa & Deco":    ["Sofá", "Mesa de Jantar", "Luminária", "Tapete", "Quadro"],
    "Esportes":       ["Bicicleta", "Halteres", "Esteira", "Tênis Esportivo", "Mochila"],
    "Beleza":         ["Perfume", "Creme Hidratante", "Maquiagem", "Shampoo", "Protetor Solar"],
}

def generate_products(n: int = 200, seed: int = 42) -> pd.DataFrame:
    """Gera catálogo de produtos da DataCommerce."""
    
    logger.info(f"Gerando {n} produtos...")
    
    Faker.seed(seed)
    random.seed(seed)
    
    products = []
    for i in range(1, n + 1):
        category    = random.choice(list(CATEGORIES.keys()))
        subcategory = random.choice(CATEGORIES[category])
        cost_price  = round(random.uniform(10, 800), 2)
        margin      = random.uniform(0.20, 0.80)
        
        products.append({
            "product_id":       f"PROD-{i:05d}",
            "name":             f"{subcategory} {fake.color_name()} {fake.word().capitalize()}",
            "category":         category,
            "subcategory":      subcategory,
            "sku":              fake.bothify("??-####-??").upper(),
            "cost_price":       cost_price,
            "sale_price":       round(cost_price * (1 + margin), 2),
            "margin_pct":       round(margin * 100, 1),
            "stock_quantity":   random.randint(0, 500),
            "supplier_id":      f"SUPP-{random.randint(1, 20):03d}",
            "is_active":        random.choices([True, False], weights=[90, 10])[0],
            "created_at":       fake.date_between(
                                    start_date="-2y", end_date="-6m"
                                ).isoformat(),
            "ingestion_at":     datetime.utcnow().isoformat(),
        })
    
    df = pd.DataFrame(products)
    logger.success(f"{len(df)} produtos gerados | "
                   f"Categorias: {df['category'].nunique()} | "
                   f"Preço médio: R$ {df['sale_price'].mean():.2f}")
    return df