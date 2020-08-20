from psycopg2 import connect

_connection = None


def _get_connection():
    global _connection
    if _connection is None:
        _connection = connect(
            user='detector',
            host='127.0.0.1',
            port=5432,
            database='detector'
        )
    return _connection


def execute_statement(statement, parameters):
    connection = _get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(statement, parameters)
        connection.commit()
    except BaseException as exception:
        print(exception)
        connection.rollback()
    finally:
        cursor.close()
