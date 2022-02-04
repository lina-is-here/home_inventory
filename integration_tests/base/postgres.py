import os

import psycopg2
import pytest


@pytest.fixture(scope="session")
def postgres_connection():
    connection_params = {
        "host": os.environ.get("POSTGRES_HOST", "hi-postgres"),
        "port": 5432,
        "database": os.environ.get("POSTGRES_DB", "data"),
        "user": os.environ.get("POSTGRES_USER", "user"),
        "password": os.environ.get("POSTGRES_PASSWORD", "verysecret"),
    }

    conn = psycopg2.connect(**connection_params)

    # Create a cursor object
    cur = conn.cursor()

    yield conn, cur

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()


def add_measurement(db_connection, db_cursor, measurement_name, is_default=False):
    # insert measurement in measurement table
    db_cursor.execute(
        """INSERT INTO inventory_measurement (name, is_default) VALUES (%s, %s);""",
        (measurement_name, is_default),
    )
    db_connection.commit()
