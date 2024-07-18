import psycopg2
import pandas as pd

def get_db_connection():
    return psycopg2.connect(
        dbname="patientcare_ab_test",
        user="your_username",  # Replace with your macOS username
        password="",
        host="localhost",
        port="5432"
    )

def execute_query(query):
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df