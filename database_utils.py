import psycopg2
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    try:
        return psycopg2.connect(
            dbname="patientcare_ab_test",
            user="[name]",
            password="[psw]",
            host="localhost",
            port="5432"
        )
    except psycopg2.Error as e:
        logging.error(f"Unable to connect to the database: {e}")
        raise

def execute_query(query):
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(query, conn)
        logging.info(f"Query executed successfully. Columns in query result: {df.columns.tolist()}")
        return df
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
        raise
    except pd.io.sql.DatabaseError as e:
        logging.error(f"Pandas SQL error: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")