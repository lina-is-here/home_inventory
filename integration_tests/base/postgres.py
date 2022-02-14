"""
All the things to talk to the database directly
"""
import os

import psycopg2
import pytest
from wait_for import wait_for


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

    # check that postgres is available and set up
    def _postgres_is_available():
        try:
            cur.execute("SELECT * FROM inventory_measurement;")
            conn.commit()
            return True
        except:  # whatever is error, try to rollback the failed transaction
            conn.rollback()
            return False

    wait_for(
        _postgres_is_available,
        delay=1,
        timeout=180,
        handle_exception=True,
    )

    yield conn, cur

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def add_pieces_measurement(postgres_connection):
    """
    Add measurement to the app
    """
    db_connection, db_cursor = postgres_connection
    db_cursor.execute(
        "INSERT INTO inventory_measurement (name, is_default) VALUES ('pieces', false);"
    )
    db_connection.commit()

    yield

    # delete all items first as they reference this measurement
    db_cursor.execute("DELETE FROM inventory_item")
    db_cursor.execute("DELETE FROM inventory_measurement WHERE name = 'pieces';")
    db_connection.commit()


@pytest.fixture(scope="session", autouse=True)
def add_default_location(postgres_connection):
    """
    Add some location
    """
    db_connection, db_cursor = postgres_connection
    db_cursor.execute("INSERT INTO inventory_location (name) VALUES ('nice place');")
    db_connection.commit()

    yield

    # delete all items first as they reference this measurement
    db_cursor.execute("DELETE FROM inventory_item")
    db_cursor.execute("DELETE FROM inventory_location WHERE name = 'nice place';")
    db_connection.commit()


@pytest.fixture()
def add_measurement(postgres_connection):
    db_connection, db_cursor = postgres_connection

    msrmnt = []

    def add_measurement_func(measurement_name, is_default=False):
        # passing measurement name to the fixture for cleanup
        msrmnt.append(measurement_name)

        # insert measurement in measurement table
        try:
            db_cursor.execute(
                "INSERT INTO inventory_measurement (name, is_default) VALUES (%s, %s);",
                (measurement_name, is_default),
            )
            db_connection.commit()
        except:
            db_connection.rollback()
            raise psycopg2.Error(
                "Error while inserting {measurement_name}, default = {is_default}"
            )

    yield add_measurement_func

    db_cursor.execute(
        "DELETE FROM inventory_measurement WHERE name = (%s);",
        (msrmnt[0],),
    )
    db_connection.commit()
