
import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="",      
            user="",
            passwd="",
            database=""
        )
        return connection
    except Error as err:
        print(f"Error connecting to the database {err}")
        return None

# Database - Note
def insert_note(title, body, user_id):
    db_connection = create_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        insert_query = f"INSERT INTO note (title, body, user_id) VALUES ({title}, {body}, {user_id})"

        cursor.execute(insert_query, (title, body, user_id))
        db_connection.commit()
        cursor.close()
        db_connection.close()

#################################
#################################

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


#################################
#################################
