import logging
from typing import Sequence

import os
import urllib.parse
from azure.identity import DefaultAzureCredential
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
        self.sslmode: str = config("PG_SSL_MODE", default="require")  # Changed default to 'require' for Azure
        self.auth_method: str = config("PG_AUTH_METHOD", default="password")  # New: 'password' or 'entra'
        self.connection = self._connect()

    def _connect(self):
        credential = DefaultAzureCredential()
        # Acquire token with the correct scope for PostgreSQL Entra auth
        token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default").token
        # Build DSN using the token as password
        dbhost = os.environ['PG_HOST']
        dbname = os.environ['PG_DATABASE']
        dbuser = urllib.parse.quote(os.environ['PG_USERNAME'])  # URL-encode username if needed
        sslmode = os.environ.get('PG_SSLMODE', 'require')  # Default to 'require' if not set
        dsn = f"host={dbhost} dbname={dbname} user={dbuser} password={token} sslmode={sslmode}"    
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
