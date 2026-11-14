"""CLI: Oracle connection test only."""

from __future__ import annotations

from pathlib import Path

import click

from db_monitor.config import load_config
from db_monitor.connectors.oracle import OracleConnector


@click.group()
@click.option(
    "--env-file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
    help="Path to .env file (default: ./.env)",
)
@click.pass_context
def cli(ctx: click.Context, env_file: Path | None) -> None:
    """Connect to a remote Oracle database."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(env_file)


@cli.command("test-connection")
@click.pass_context
def test_connection(ctx: click.Context) -> None:
    """Connect to Oracle and print a simple server check."""
    cfg = ctx.obj["config"]
    if cfg.dsn:
        mode = f"dsn={cfg.dsn}"
    elif cfg.service:
        mode = f"service_name={cfg.service}"
    else:
        mode = f"sid={cfg.sid}"
    click.echo(f"Connecting to {cfg.host}:{cfg.port} ({mode})")
    with OracleConnector(cfg) as db:
        rows = db.query(
            "SELECT SYS_CONTEXT('USERENV','DB_NAME') AS db_name, "
            "SYS_CONTEXT('USERENV','SERVER_HOST') AS host, "
            "SYSDATE AS server_time FROM dual"
        )
    row = rows[0] if rows else {}
    click.echo(f"db_name     : {row.get('db_name')}")
    click.echo(f"host        : {row.get('host')}")
    click.echo(f"server_time : {row.get('server_time')}")
    click.echo("Connection OK")


def main() -> None:
    try:
        cli(obj={})
    except ValueError as exc:
        click.echo(f"Config error: {exc}", err=True)
        raise SystemExit(2) from exc
    except Exception as exc:  # noqa: BLE001
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
