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

        # User authentication
        username = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()

        # Verify user credentials (we may need to implement a more secure authentication mechanism)
        if authenticate_user(username, password):
            print(f"Authentication successful for {username}")
            users[username] = {'socket': client_socket, 'notes': []}

            # Handle user commands (create, list, delete notes, etc.)
            handle_user_commands(username, users)
        else:
            print(f"Authentication failed for {username}")
            client_socket.sendall("Authentication failed".encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

# Add functions for user authentication and handling user commands
def authenticate_user(username, password):
    # Implement your authentication logic (e.g., check against a user database)
    return True  # Replace with actual authentication logic

def handle_user_commands(username, users):
    client_socket = users[username]['socket']

    while True:
        # Receive user commands and perform actions
        command = client_socket.recv(1024).decode()        
        if command.startswith("CREATE_NOTE"):
            note_title = command.split(":")[1]
            note_content = command.split(":")[2]
            create_note(username, note_title, note_content, users)
        elif command.startswith("LIST_NOTES"):
            list_notes(username, users)
        elif command.startswith("LIST_NOTE"):
            note_index = int(command.split(":")[1])
            list_note(username, note_index, users)
        elif command.startswith("DELETE_NOTE"):
            note_index = int(command.split(":")[1])
            delete_note(username, note_index, users)
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
        print(notes)
        client_socket.sendall(notes.encode())

def list_note(username, note_id, user_id, users):
    client_socket = users[username]['socket'] # debug here
    try:
        note = database.get_note(note_id, 1)
        print(note)
        client_socket.sendall(note.encode())
    except:
        client_socket.sendall("Something went wrong.".encode())


def delete_note(username, note_id, user_id):
    try:
        database.delete_note(note_id, user_id)
        print(f"\nNote deleted for {username}\n")
    except IndexError:
        print(f"Invalid note id for deletion")