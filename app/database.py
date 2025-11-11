import psycopg2
from psycopg2 import pool
import logging

class PostgresDB:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection_pool = None

    def initialize_pool(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,  # Minimum and maximum number of connections in the pool
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db_name
            )
            logging.info("Connection pool created successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"Error while creating connection pool: {error}")

    def get_connection(self):
        try:
            connection = self.connection_pool.getconn()
            if connection:
                return connection
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"Error while getting connection: {error}")

    def release_connection(self, connection):
        try:
            self.connection_pool.putconn(connection)
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"Error while releasing connection: {error}")

    def close_all_connections(self):
        try:
            if self.connection_pool:
                self.connection_pool.closeall()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"Error while closing connection pool: {error}")

    def execute_query(self, query, params=None):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            if cursor.description:
                result = cursor.fetchall()
            else:
                result = None
            conn.commit()
            return result
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.release_connection(conn)
