
import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="password",
            database="notes"
        )
        return connection
    except Error as err:
        print(f"Error connecting to the database {err}")
        return None

def perform_query(query, params):
    db_connection = create_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        try:
            cursor.execute(query, params)
            db_connection.commit()
            cursor.close()
            db_connection.close()
        except Error as err:
            print(f"Error connecting to the database {err}")
            return None

def insert_note(title, body, user_id):
    query = "INSERT INTO note (title, description, user_id) VALUES (%s, %s, %s)"
    perform_query(query, (title, body, user_id))

# Database - User
def insert_user(username, password):
    db_connection = create_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        insert_query = """
        INSERT INTO user (username, password) VALUES (%s, %s)
        """
        cursor.execute(insert_query, (username, password))
        db_connection.commit()
        cursor.close()
        db_connection.close()

