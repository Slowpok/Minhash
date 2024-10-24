import datetime
from psycopg2 import Error
import env
import psycopg2
import psycopg2.extras


def execute_insert_query(connection, data):
    cursor = connection.cursor()
    query = "INSERT INTO people (id, all_hash, bucket_hash, buckets) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, data)
        connection.commit()
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def mass_insert_to_db(connection, cursor, data):
    try:
        clear_minhash_table(connection, cursor)

        args_str = ','.join(cursor.mogrify("(%s, %s, %s, %s)", x).decode('utf-8') for x in data)

        cursor.execute("INSERT INTO minhashtable (element_id, all_hash, hash_buckets, buckets) VALUES " + args_str)
        connection.commit()

    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, cursor, element_id):

    query = "SELECT * FROM minhashtable WHERE %s = ANY (buckets)"

    try:
        cursor.execute(query, (element_id, ))
        result = cursor.fetchall()
        return result
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        return None


def clear_minhash_table(connection, cursor):
    query = ''' DELETE FROM minhashtable '''
    try:
        cursor.execute(query)
        connection.commit()
        return True
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        return False
