from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# Caminho da raiz do projeto, calculado a partir deste arquivo
# config.py está em src/ingestion/config.py, então sobe 2 níveis
PROJECT_ROOT = Path(__file__).resolve().parents[2]

@dataclass
class DataConfig:
    """Configurações de geração de dados da DataCommerce."""
    
    # Volume de dados
    num_customers: int = 1_000
    num_products:  int = 200
    num_orders:    int = 5_000
    num_events:    int = 20_000
    
    # Caminho de saída — sempre relativo à raiz do projeto, 
    # independente de onde o script é executado
    output_path: str = str(PROJECT_ROOT / "data" / "raw")
    
    # Seed para reprodutibilidade
    random_seed: int = 42

config = DataConfig()