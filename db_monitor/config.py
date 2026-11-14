"""Load Oracle connection settings from .env."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import oracledb
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class OracleConfig:
    host: str
    port: int
    user: str
    password: str
    service: str | None = None
    sid: str | None = None
    dsn: str | None = None

    def connect_dsn(self) -> str:
        """Build DSN: ORACLE_DSN wins, else service name, else SID."""
        if self.dsn:
            return self.dsn
        if self.service:
            # Easy Connect with service name: host:port/service
            return oracledb.makedsn(self.host, self.port, service_name=self.service)
        if self.sid:
            # Connect descriptor with SID: host:port:sid style via makedsn
            return oracledb.makedsn(self.host, self.port, sid=self.sid)
        raise ValueError(
            "Set ORACLE_SERVICE (service name) or ORACLE_SID (SID), or ORACLE_DSN"
        )


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def load_config(env_file: str | Path | None = None) -> OracleConfig:
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv(_PROJECT_ROOT / ".env")

    user = os.getenv("ORACLE_USER", "").strip()
    password = os.getenv("ORACLE_PASSWORD", "").strip()
    if not user:
        raise ValueError("Missing required setting: ORACLE_USER")
    if not password:
        raise ValueError("Missing required setting: ORACLE_PASSWORD")

    service = _blank_to_none(os.getenv("ORACLE_SERVICE"))
    sid = _blank_to_none(os.getenv("ORACLE_SID"))
    dsn = _blank_to_none(os.getenv("ORACLE_DSN"))

    if not dsn and not service and not sid:
        raise ValueError(
            "Provide one of: ORACLE_SERVICE, ORACLE_SID, or ORACLE_DSN"
        )

    # If both service and SID are set, service name wins (clearer for PDBs).
    if service and sid:
        sid = None

    return OracleConfig(
        host=os.getenv("ORACLE_HOST", "localhost").strip(),
        port=int(os.getenv("ORACLE_PORT", "1521")),
        user=user,
        password=password,
        service=service,
        sid=sid,
        dsn=dsn,
    )
