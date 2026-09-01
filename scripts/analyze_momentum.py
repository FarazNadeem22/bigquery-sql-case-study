"""
Pull the GDP growth momentum query sesult from BigQuery into a pandas Dataframe
"""
from pathlib import Path
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "placeholder"
QUERY_PATH = Path(__file__).parent.parent / "queries" / "01_gdp_growth_momentum.sql"

def load_data(query_path: Path) -> pd.DataFrame:
    client = bigquery.Client()
    query = query_path.read_text()
    return client.query(query).to_dataframe()

if __name__ == "__main__":
    df = load_data(QUERY_PATH)
    print(df)