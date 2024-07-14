import os
from psycopg2 import pool
from dotenv import load_dotenv
from datetime import datetime
from catdel.state_manager import StateManager

sm = StateManager.get_instance()

def connect_to_db():
    # Load .env file
    load_dotenv()
    # Get the connection string from the environment variable
    connection_string = os.getenv('DATABASE_URL')
    # Create a connection pool
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections in the pool
        1,  # Maximum number of connections in the pool
        connection_string
    )

    # Get a connection from the pool
    conn = connection_pool.getconn()

    return conn


def save_to_feature_request(data):
    '''
    CREATE TABLE feature_requests (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    feature_title VARCHAR(255),
    feature_description TEXT,
    priority VARCHAR(50),
    timestamp TIMESTAMP
    );
    '''
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


# Function to save a record in PostgreSQL
def log(function, log_message):
    '''
    CREATE TABLE log (
    id SERIAL PRIMARY KEY,
    function TEXT NOT NULL,
    log_message TEXT NOT NULL,
    filename TEXT NOT NULL DEFAULT 'NONE',
    call_time TIMESTAMP NOT NULL,
    session_id TEXT NOT NULL,
    session_start_time TIMESTAMP NOT NULL
    );'''
    conn = connect_to_db()
    cursor = conn.cursor()
    call_time = datetime.now()
    filename = sm.uploaded_file.name if sm.uploaded_file else 'NONE'
    cursor.execute("INSERT INTO log (function, log_message, filename, call_time,  session_id, session_start_time) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (function, log_message, filename, call_time, sm.seession_id, sm.session_start_time))
    conn.commit()
    cursor.close()
    conn.close()