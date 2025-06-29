# PostgreSQL Exec SP

A lightweight Python utility to execute PostgreSQL stored procedures, mirroring the architecture of the original **MSSQL Exec SP** app.

## Features

* Executes **stored procedures** on PostgreSQL databases via `CALL proc_name(...)`.
* Environment‑driven configuration using **python‑decouple**.
* Optional argument passing via `SP_ARGS=arg1,arg2,...`.
* Packaged with a **slim Docker image** for easy CI/CD.
* Clean, minimal codebase — only ~100 lines.

## Quick Start

```bash
# 1. Clone & enter
git clone <repo-or-path> pg-exec-sp && cd pg-exec-sp

# 2. Configure
cp .env.sample .env        # then edit values

# 3. Local run
pip install -r requirements.txt
python main.py
```

Or via Docker:

```bash
docker build -t pg-exec-sp .
docker run --env-file .env --network host pg-exec-sp
```

## Environment Variables

| Variable      | Description                               | Default |
|---------------|-------------------------------------------|---------|
| `PG_HOST`     | PostgreSQL server hostname/IP             | `localhost` |
| `PG_PORT`     | PostgreSQL port                           | `5432` |
| `PG_DATABASE` | Target database                           | — |
| `PG_USERNAME` | DB user                                   | — |
| `PG_PASSWORD` | DB user password                          | — |
| `PG_SSL_MODE` | `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full` | `prefer` |
| `SP_NAME`     | Stored procedure name                     | — |
| `SP_ARGS`     | *Optional* comma‑separated list of args   | (none) |

## Extending

* If your procedure returns a result set, adapt `database/connection.py → execute()` to `fetchall()` and return rows.
* For advanced auth (IAM, Kerberos, etc.), swap `psycopg.connect` parameters accordingly.

## License

MIT
