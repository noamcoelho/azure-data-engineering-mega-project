"""
Carrega os datasets gerados (csv/parqet) em um banco SQLite local para fins de prática de SQL e testes de transformação. 
"""
import sqlite3
import pandas as pd
import glob
from pathlib import Path
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH      = PROJECT_ROOT / "data" / "datacomerce.db"
RAW_PATH     = PROJECT_ROOT / "data" / "raw"

TABLES = ["customers", "products", "orders", "order_items", "payments", "events"]

def load_latest_parquet(name: str) -> pd.DataFrame:
    pattern = str(RAW_PATH / f"{name}_*.parquet")
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado para: {pattern}")
    return pd.read_parquet(files[-1])

def main() -> None:
    logger.info(f"Criando banco SQLite em: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    for table in TABLES:
        df = load_latest_parquet(table)
        df.to_sql(table, conn, if_exists="replace", index=False)
        logger.success(f"Tabela '{table}' carregada: {len(df):,} linhas")
    
    conn.close()
    logger.info("Banco SQLite pronto para uso!")

if __name__ == "__main__":
    main()