import os
import mysql.connector

def _get_required_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value


def get_db_connection():
    connection = mysql.connector.connect(
        host=_get_required_env('DB_HOST'),
        user=_get_required_env('DB_USER'),
        password=_get_required_env('DB_PASSWORD'),
        database=_get_required_env('DB_NAME')
    )
    return connection
