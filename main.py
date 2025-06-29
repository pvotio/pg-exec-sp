import logging
from decouple import config

from database.connection import PostgreSQLDatabase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

SP_NAME = config("SP_NAME", default=None, cast=str)
SP_ARGS = config("SP_ARGS", default="", cast=str)

if SP_NAME is None or SP_NAME.strip() == "":
    logger.error("Environment variable SP_NAME is required.")
    raise SystemExit(1)

def main(sp_name: str, args: list[str]) -> None:
    pg = PostgreSQLDatabase()
    pg.execute(sp_name, args)

if __name__ == "__main__":
    arg_list = [a.strip() for a in SP_ARGS.split(",") if a.strip()]
    logger.info("Starting execution for %s with args %s", SP_NAME, arg_list)
    main(SP_NAME, arg_list)
    logger.info("Finished.")
