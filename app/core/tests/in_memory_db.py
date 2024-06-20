import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_in_memory_db():
    # Connection to the default database
    connection = psycopg2.connect(
        dbname='postgres',
        user='your_username',
        password='your_password',
        host='localhost'
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    # Create a temporary database
    temp_db_name = 'test_db'
    cursor.execute(f'CREATE DATABASE {temp_db_name};')
    cursor.close()
    connection.close()

    # Connect to the temporary database
    temp_db_connection = psycopg2.connect(
        dbname=temp_db_name,
        user='your_username',
        password='your_password',
        host='localhost'
    )

    yield temp_db_connection

    # Tear down: close connection and drop the temporary database
    temp_db_connection.close()
    connection = psycopg2.connect(
        dbname='postgres',
        user='your_username',
        password='your_password',
        host='localhost'
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(f'DROP DATABASE {temp_db_name};')
    cursor.close()
    connection.close()
