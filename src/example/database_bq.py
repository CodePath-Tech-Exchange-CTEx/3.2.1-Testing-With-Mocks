from __future__ import annotations

from typing import Iterable, Mapping, Any, List, Dict

from google.cloud import bigquery


class DatabaseBQ:
    """Small BigQuery-backed database wrapper for expenses.

    This mirrors the slide-style API: Database.connect("expenses").read_rows().
    """

    def __init__(self, project_id: str, dataset: str, table: str) -> None:
        # Slides 3–6: this object represents the "read from database" step.
        self._project_id = project_id
        self._dataset = dataset
        self._table = table
        # Slide 10: Identify dependencies — this class wraps network I/O.
        self._client = bigquery.Client(project=project_id)

    @classmethod
    def connect(cls, name: str, config: Mapping[str, Mapping[str, Any]]) -> "DatabaseBQ":
        """Create a DatabaseBQ from a named config section.

        Expected config shape (example):
        {
            "expenses": {
                "project_id": "...",
                "dataset": "...",
                "table": "..."
            }
        }
        """
        section = config[name]
        return cls(
            project_id=str(section["project_id"]),
            dataset=str(section["dataset"]),
            table=str(section["table"]),
        )

    def read_rows(self) -> List[Dict[str, object]]:
        """Read all expense rows from BigQuery.

        Returns a list of plain dicts with keys:
        - vendor
        - amount
        - currency
        """
        table_id = f"{self._project_id}.{self._dataset}.{self._table}"

        # Use a table reference + list_rows instead of string-building SQL.
        # This gives us a safe table reference construction.
        table = self._client.get_table(table_id)

        rows: Iterable[bigquery.Row] = self._client.list_rows(
            table,
            selected_fields=[
                bigquery.SchemaField("vendor", "STRING"),
                bigquery.SchemaField("amount", "FLOAT"),
                bigquery.SchemaField("currency", "STRING"),
            ],
        )

        results: List[Dict[str, object]] = []
        for row in rows:
            results.append(
                {
                    "vendor": row["vendor"],
                    "amount": float(row["amount"]) if row["amount"] is not None else 0.0,
                    "currency": row["currency"],
                }
            )
        return results

