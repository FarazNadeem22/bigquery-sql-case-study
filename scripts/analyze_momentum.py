"""
Pull the GDP growth momentum query result from BigQuery into a pandas Dataframe
"""
from pathlib import Path
import pandas as pd
from google.cloud import bigquery
import time
import subprocess
import os

PROJECT_ID = "placeholder"
QUERY_PATH = Path(__file__).parent.parent / "queries" / "01_gdp_growth_momentum.sql"

def load_data(query_path: Path) -> pd.DataFrame:
    client = bigquery.Client()
    query = query_path.read_text()
    return client.query(query).to_dataframe()

def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Average growth rank and growth rate per county, across all years. 
    lower ave_growth_rank = more consistently streong growth momentum
    """
    summary = (
        df.groupby(["country_name", "country_code"])
        .agg(
            avg_growth_rank =("growth_rank_that_year", "mean"),
            avg_gdp_growth_pct = ("gdp_growth_pct", "mean"),
        )
        .reset_index()
        .sort_values("avg_growth_rank")
        .reset_index(drop=True)
    )
    # summary["Rank"] = range(1, len(summary)+1)
    summary.insert(0, "rank", range( 1, len(summary) + 1))
    return summary

def clear_screen():
    if os.name == 'nt':
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])

def run():
    df = load_data(QUERY_PATH)
    summary = summarize(df)
    print(df)
    time.sleep(1)
    clear_screen()
    print(summary)

if __name__ == "__main__":
    run()
