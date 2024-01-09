# server.py - This is the main server module responsible for handling client connections.
import threading
from Application.network import create_socket, bind_socket, listen

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
            note_content = command.split(":")[1]
            create_note(username, note_content, users)
        elif command.startswith("LIST_NOTES"):
            list_notes(username, users)
        elif command.startswith("DELETE_NOTE"):
            note_index = int(command.split(":")[1])
            delete_note(username, note_index, users)
        elif command.startswith("GET_AUTH"):
            client_socket.sendall(username.encode())

        # Add more commands as needed

def create_note(username, note_content, users):
    users[username]['notes'].append(note_content)
    print(f"\nNote created for {username}\n")

def list_notes(username, users):
    client_socket = users[username]['socket']
    notes = users[username]['notes']
    notes_str = "\n".join([f"{index + 1}. {note}" for index, note in enumerate(notes)])
    client_socket.sendall(notes_str.encode())

def delete_note(username, note_index, users):
    try:
        users[username]['notes'].pop(note_index - 1)
        print(f"\nNote deleted for {username}\n")
    except IndexError:
        print(f"Invalid note index for deletion")
