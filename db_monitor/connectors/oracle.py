"""Oracle connector using python-oracledb (thin mode)."""

from __future__ import annotations

from typing import Any

import oracledb

from db_monitor.config import OracleConfig


class OracleConnector:
    def __init__(self, config: OracleConfig) -> None:
        self._config = config
        self._conn: oracledb.Connection | None = None

    def connect(self) -> None:
        self._conn = oracledb.connect(
            user=self._config.user,
            password=self._config.password,
            dsn=self._config.connect_dsn(),
        )

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def query(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        if self._conn is None:
            raise RuntimeError("Not connected. Call connect() first.")
        with self._conn.cursor() as cur:
            cur.execute(sql, params or {})
            if cur.description is None:
                return []
            columns = [col[0].lower() for col in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]

    def __enter__(self) -> OracleConnector:
        self.connect()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
