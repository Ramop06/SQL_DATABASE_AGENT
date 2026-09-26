from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.config import DATABASE_URL


# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


def get_engine() -> Engine:
    return engine


def get_schema() -> str:
    """
    Return the database schema as text.
    """

    schema = []

    with engine.connect() as connection:

        # Get all user tables
        result = connection.execute(
            text("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
        )

        tables = [row[0] for row in result]

        for table in tables:

            columns_result = connection.execute(
                text(f'PRAGMA table_info("{table}")')
            )

            columns = []

            for column in columns_result:
                column_name = column[1]
                column_type = column[2]

                columns.append(
                    f"{column_name} {column_type}"
                )

            schema.append(
                f"TABLE {table} ({', '.join(columns)})"
            )

    if not schema:
        return "No tables exist in the database."

    return "\n".join(schema)


def execute_sql(sql: str):
    """
    Execute a SELECT SQL query and return rows.
    """

    sql = sql.strip()

    # Security: this application should only execute SELECT queries
    if not sql.upper().startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    with engine.connect() as connection:

        result = connection.execute(text(sql))

        rows = result.fetchall()
        columns = result.keys()

        return [
            dict(zip(columns, row))
            for row in rows
        ]