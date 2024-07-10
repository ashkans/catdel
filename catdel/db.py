import os
from psycopg2 import pool
from dotenv import load_dotenv


def connect_to_db():
    # Load .env file
    load_dotenv()
    # Get the connection string from the environment variable
    connection_string = os.getenv('DATABASE_URL')
    # Create a connection pool
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections in the pool
        10,  # Maximum number of connections in the pool
        connection_string
    )
    # Check if the pool was created successfully
    if connection_pool:
        print("Connection pool created successfully")
    # Get a connection from the pool
    conn = connection_pool.getconn()

    return conn


def save_to_db(data):
    conn = connect_to_db()
    cur = conn.cursor()
    insert_query = """
    INSERT INTO feature_requests (user_name, user_email, feature_title, feature_description, priority, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(insert_query, (
        data['user_name'],
        data['user_email'],
        data['feature_title'],
        data['feature_description'],
        data['priority'],
        data['Timestamp']
    ))
    conn.commit()
    cur.close()
    conn.close()


def fetch_data_from_db():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM feature_requests")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return rows, columns