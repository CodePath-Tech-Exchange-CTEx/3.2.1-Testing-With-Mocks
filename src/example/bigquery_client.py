from __future__ import annotations

from typing import Iterable

from google.cloud import bigquery


def fetch_expense_rows(
    project_id: str,
    dataset: str,
    table: str,
    client: bigquery.Client | None = None,
) -> Iterable[dict]:
    """Fetch expense rows from BigQuery.

    In tests, you will typically **mock** this function or pass in a fake
    `client` so that no real network calls are made.
    """
    if client is None:
        client = bigquery.Client(project=project_id)

    table_ref = f"{project_id}.{dataset}.{table}"
    query = f"SELECT category, amount FROM `{table_ref}`"

    job = client.query(query)
    return (dict(row) for row in job.result())

