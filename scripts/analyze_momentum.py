"""
Pull the revenue-momentum query result from BigQuery into pandas, summarize,
and chart it. Fill in PROJECT_ID and the query file path once your BigQuery
sandbox is set up (Week 1 of the course).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "your-project-id"
QUERY_PATH = Path(__file__).parent.parent / "queries" / "01_revenue_momentum.sql"


def load_data(project_id: str, query_path: Path) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = query_path.read_text()
    return client.query(query).to_dataframe()


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Average momentum rank and growth by sector, most recent quarter first."""
    return (
        df.groupby(["sector", "fiscal_quarter"])
        .agg(avg_qoq_growth=("qoq_growth", "mean"), n_companies=("company_name", "count"))
        .reset_index()
        .sort_values(["fiscal_quarter", "avg_qoq_growth"], ascending=[False, False])
    )


def plot_sector_momentum(summary: pd.DataFrame, out_path: Path) -> None:
    latest_quarter = summary["fiscal_quarter"].max()
    latest = summary[summary["fiscal_quarter"] == latest_quarter]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(latest["sector"], latest["avg_qoq_growth"])
    ax.set_xlabel("Avg QoQ revenue growth")
    ax.set_title(f"Sector revenue momentum — {latest_quarter}")
    ax.axvline(0, color="black", linewidth=0.8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)


def main() -> None:
    df = load_data(PROJECT_ID, QUERY_PATH)
    summary = summarize(df)
    print(summary.to_string(index=False))

    out_path = Path(__file__).parent.parent / "sector_momentum.png"
    plot_sector_momentum(summary, out_path)
    print(f"\nChart saved to {out_path}")


if __name__ == "__main__":
    main()
