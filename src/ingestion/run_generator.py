"""
Script principal de geração de dados sintéticos da DataCommerce.
Executa todos os geradores e salva os dados em data/raw/.
"""
import os
import pandas as pd
from loguru import logger
from datetime import datetime

from generators.customers import generate_customers
from generators.products   import generate_products
from generators.orders     import generate_orders
from generators.payments   import generate_payments
from generators.events     import generate_events
from config                import config

def save_dataset(df: pd.DataFrame, name: str, fmt: str = "csv") -> None:
    """Salva dataset em CSV e Parquet."""
    
    os.makedirs(config.output_path, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    
    if fmt in ("csv", "both"):
        path = f"{config.output_path}/{name}_{timestamp}.csv"
        df.to_csv(path, index=False)
        logger.info(f"CSV salvo: {path} ({len(df):,} linhas)")
    
    if fmt in ("parquet", "both"):
        path = f"{config.output_path}/{name}_{timestamp}.parquet"
        df.to_parquet(path, index=False, compression="snappy")
        logger.info(f"Parquet salvo: {path}")

def main() -> None:
    logger.info("=== DataCommerce — Gerador de dados sintéticos ===")
    start = datetime.utcnow()
    
    # Clientes
    customers_df = generate_customers(config.num_customers, config.random_seed)
    save_dataset(customers_df, "customers", fmt="both")
    
    # Produtos
    products_df = generate_products(config.num_products, config.random_seed)
    save_dataset(products_df, "products", fmt="both")
    
    # Pedidos (depende de customers e products)
    customer_ids = customers_df["customer_id"].tolist()
    product_ids  = products_df["product_id"].tolist()
    orders_df, items_df = generate_orders(
        config.num_orders, customer_ids, product_ids, config.random_seed
    )
    save_dataset(orders_df, "orders",      fmt="both")
    save_dataset(items_df,  "order_items", fmt="both")
    
    # Pagamentos (depende de orders)
    payments_df = generate_payments(orders_df, config.random_seed)
    save_dataset(payments_df, "payments", fmt="both")
    
    # Eventos de navegação (depende de customers e products)
    events_df = generate_events(
        config.num_events, customer_ids, product_ids, config.random_seed
    )
    save_dataset(events_df, "events", fmt="both")
    
    elapsed = (datetime.utcnow() - start).seconds
    logger.success(f"=== Geração concluída em {elapsed}s ===")
    logger.info(f"Arquivos disponíveis em: {config.output_path}/")

if __name__ == "__main__":
    main()