
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

def execute_query(query, params, isSelectQuery):
    result = ''
    db_connection = create_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        try:
            cursor.execute(query, params)
            if isSelectQuery:
                result = get_query_result(cursor)
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return result
        except Error as err:
            print(f"Error connecting to the database {err}")
            return None

def insert_note(title, body, user_id):
    query = "INSERT INTO note (title, description, user_id) VALUES (%s, %s, %s)"
    return execute_query(query, (title, body, user_id), False)

# Database - User
def insert_user(username, password):
    query = "INSERT INTO user (username, password) VALUES (%s, %s)"
    return execute_query(query, (username, password), False)

def list_all_user_notes(user_id):
    query = "SELECT id, title, description FROM note WHERE user_id = %s"
    return execute_query(query, (user_id,), True)

def get_note(note_id, user_id):
    query = "SELECT id, title, description FROM note WHERE id = %s and user_id = %s"
    return execute_query(query, (note_id, user_id), True)

def delete_note(note_id, user_id):
    query = "DELETE FROM note WHERE id = %s AND user_id = %s"
    return execute_query(query, (note_id, user_id), False)

def get_query_result(cursor):
    result = ''
    for (id, title, description) in cursor:
        result += "Note id: {} \n  Title: {} \n  Description: {}\n".format(id, title, description)
    return result