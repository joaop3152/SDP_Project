# client.py - This module is responsible for client-side functionality.
from Application.network import *

def connect_to_server(host, port):
    client_socket = create_socket()
    client_socket.connect((host, port))
    return client_socket

def send_name(client_socket, username, password):
    client_socket.sendall(username.encode())
    client_socket.sendall(password.encode())

def create_note(client_socket, note_content):
    client_socket.sendall(f"CREATE_NOTE:{note_content}".encode())
    print(f"\nNote created!\n")
    input("Press Enter to continue...")

def list_notes(client_socket):
    client_socket.sendall("LIST_NOTES".encode())
    data = client_socket.recv(1024)
    print(f"\nYour Notes:\n{data.decode()}\n")
    input("Press Enter to continue...")

def list_notes_to_erase(client_socket):
    client_socket.sendall("LIST_NOTES".encode())
    data = client_socket.recv(1024)
    print(f"\nYour Notes:\n{data.decode()}\n")

def delete_note(client_socket, note_index):
    client_socket.sendall(f"DELETE_NOTE:{note_index}".encode())
    print(f"\nNote deleted successfully\n")
    input("Press Enter to continue...")