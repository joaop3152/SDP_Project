
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

# def insert_message(sender, receiver, message): change to our app 
#     db_connection = create_db_connection()
#     if db_connection is not None:
#         cursor = db_connection.cursor()
#         insert_query = """
#         INSERT INTO messages (sender, receiver, message) VALUES (%s, %s, %s)
#         """
#         cursor.execute(insert_query, (sender, receiver, message))
#         db_connection.commit()
#         cursor.close()
#         db_connection.close()
