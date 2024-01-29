# server.py - This is the main server module responsible for handling client connections.
import threading
from Application.network import create_socket, bind_socket, listen
from Model import database

def start_server(host, port):
    server_socket = create_socket()
    bind_socket(server_socket, host, port)
    listen(server_socket)
    print(f"Server ready to receive connections on {host}:{port}...")

    clients = {}

    while True:
        conn, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(conn, addr, clients))
        client_handler.start()

def handle_client(client_socket, client_address, users):
    try:
        print(f"Connection established with {client_address}")

        request = client_socket.recv(1024).decode().split(':')

        username = request[0]
        password = request[1]
        mode = request[2]

        # Verify user credentials (we may need to implement a more secure authentication mechanism)
        if authenticate_user(username, password, mode):
            print(f"Authentication successful for {username}")
            client_socket.sendall(username.encode())

            users[username] = {'socket': client_socket, 'notes': []}

            user_id = database.search_user(username)
            
            # Handle user commands (create, list, delete notes, etc.)
            handle_user_commands(username, users, user_id)
        else:
            print(f"Authentication failed for {username}")
            client_socket.sendall("AUTH_FAILED".encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

# Add functions for user authentication and handling user commands
def authenticate_user(username, password, mode): ## mode 0 is register and mode 1 is auth
    # CASES:    
    if(database.search_user(username) == -1 and mode == 'register'): #   username dont exist then register
        database.insert_user(username, password)
        return True
    else:
        if(mode == 'register'): # trying to register a existing username
            return False
        #   username exist but password dont match
        if(database.search_user(username,2) != password):
            return False
        

    return True

def handle_user_commands(username, users, user_id):
    client_socket = users[username]['socket']

    while True:
        # Receive user commands and perform actions
        command = client_socket.recv(1024).decode()        
        if command.startswith("CREATE_NOTE"):
            note_title = command.split(":")[1]
            note_content = command.split(":")[2]
            create_note(username, note_title, note_content, user_id)
        elif command.startswith("LIST_NOTES"):
            list_notes(username, user_id, users)
        elif command.startswith("LIST_NOTE"):
            note_index = int(command.split(":")[1])
            list_note(username, note_index, user_id, users)
        elif command.startswith("DELETE_NOTE"):
            note_index = int(command.split(":")[1])
            delete_note(username, note_index, user_id)
        elif command.startswith("GET_AUTH"):
            client_socket.sendall(username.encode())

        # Add more commands as needed

def create_note(username, note_title, note_content, user_id):
    database.insert_note(note_title, note_content, user_id)
    print(f"\nNote created for {username}\n")

def list_notes(username, user_id, users):
    client_socket = users[username]['socket']
    notes = database.list_all_user_notes(user_id)

    if len(notes) == 0:
        client_socket.sendall("No notes.".encode())
    else:
        client_socket.sendall(get_query_result(notes).encode())

def list_note(username, note_id, user_id, users):
    client_socket = users[username]['socket'] # debug here
    try:
        note = database.get_note(note_id, user_id)
        client_socket.sendall(get_query_result(note).encode())
    except:
        client_socket.sendall("Something went wrong.".encode())

def delete_note(username, note_id, user_id):
    try:
        database.delete_note(note_id, user_id)
        print(f"\nNote deleted for {username}\n")
    except IndexError:
        print(f"Invalid note id for deletion")

def get_query_result(cursor):
    result = ''
    for i in cursor:
        result += "Note id: {} \n  Title: {} \n  Description: {}\n".format(i[0], i[1], i[2])
    return result