import logging
from typing import Sequence

import psycopg
from decouple import config

logger = logging.getLogger(__name__)

class PostgreSQLDatabase:
    """Simple helper around psycopg for executing stored procedures."""

    def __init__(self) -> None:
        self.host: str = config("PG_HOST", default="localhost")
        self.port: int = config("PG_PORT", cast=int, default=5432)
        self.database: str = config("PG_DATABASE", default="postgres")
        self.username: str = config("PG_USERNAME", default="postgres")
        self.password: str = config("PG_PASSWORD", default="")
        self.sslmode: str = config("PG_SSL_MODE", default="prefer")
        self.connection = self._connect()

    def _connect(self):
        dsn = (
            f"host={self.host} port={self.port} dbname={self.database} "
            f"user={self.username} password={self.password} sslmode={self.sslmode}"
        )
        logger.info("Connecting to PostgreSQL at %s:%s/%s", self.host, self.port, self.database)
        conn = psycopg.connect(dsn, autocommit=True)
        return conn

    def execute(self, sp_name: str, args: Sequence[str] | None = None) -> bool:
        """Execute a stored procedure (CALL). Args are passed positionally."""
        args = args or []
        placeholders = ", ".join(["%s"] * len(args))
        call_stmt = f"CALL {sp_name}({placeholders});" if placeholders else f"CALL {sp_name}();"

        logger.info("Executing stored procedure: %s", call_stmt)
        try:
            with self.connection.cursor() as cur:
                cur.execute(call_stmt, args)
            logger.info("Procedure executed successfully.")
            return True
        except Exception as exc:
            logger.exception("Failed to execute stored procedure.")
            raise exc
