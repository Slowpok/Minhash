import psycopg2
import env
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_new_db():
    result = False
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=env.user,
                                      # пароль, который указали при установке PostgreSQL
                                      password=env.password,
                                      host=env.host,
                                      port=env.port)
                                      # client_encoding="windows-1251",
                                      # options="-c client_encoding=UTF8")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_create_database = 'create database ' + env.name_db
        cursor.execute(sql_create_database)
        result = True
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return result

def connection_db():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=env.user,
                                      password=env.password,
                                      host=env.host,
                                      port=env.port,
                                      database=env.name_db)
                                      # client_encoding="UTF-8",
                                      # options="-c client_encoding=UTF8")

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")
        return {'connection': connection, 'cursor': cursor}
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        return None


def create_table():
    resultconnection = connection_db()
    if resultconnection is None:
        print("Ошибка при подключении к базе данных")
        return None

    connection = resultconnection['connection']
    cursor = resultconnection['cursor']

    # table training
    try:
        # SQL-запрос для создания новой таблицы
        create_table_query = '''CREATE TABLE IF NOT EXISTS minhashtable
                              (element_id   UUID PRIMARY KEY NOT NULL,
                              all_hash      int[],
                              hash_buckets  int[][],
                              buckets       UUID[])'''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица min_hash_table успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при создании таблицы min_hash_table", error)

    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")


