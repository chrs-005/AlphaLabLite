import json
import sqlite3
import uuid
from pathlib import Path


class Storage:
    def __init__(self, db_path="alphalablite.db"):
        project_folder = Path(__file__).parent
        self.db_path = project_folder / db_path
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS saved_series (
                    execution_id TEXT NOT NULL,
                    variable_name TEXT NOT NULL,
                    series_json TEXT NOT NULL
                )
                """
            )

    def save_execution(self, variables):
        # Save every computed variable under one execution id

        execution_id = str(uuid.uuid4())

        with sqlite3.connect(self.db_path) as connection:
            for variable_name, series in variables.items():
                connection.execute(
                    """
                    INSERT INTO saved_series (execution_id, variable_name, series_json)
                    VALUES (?, ?, ?)
                    """,
                    (execution_id, variable_name, json.dumps(series)),
                )

        return execution_id

    def load_items(self, execution_id, item_names):
        if not item_names:
            return {}

        variablenames = ",".join(["?"] * len(item_names))
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                f"""
                SELECT variable_name, series_json
                FROM saved_series
                WHERE execution_id = ?
                AND variable_name IN ({variablenames})
                """,
                [execution_id, *item_names],
            ).fetchall()

        items = {}
        for variable_name, series_json in rows:
            items[variable_name] = json.loads(series_json)

        return items
