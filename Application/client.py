# client.py - This module is responsible for client-side functionality.
from Application.network import *

def connect_to_server(host, port):
    client_socket = create_socket()
    client_socket.connect((host, port))
    return client_socket

def get_loadbalancer_port(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', port))

    # Receive data from the server
    data_received = client_socket.recv(1024).decode()
    print(f"Received data from server: {data_received}")

    # Close the connection
    client_socket.close()

    return data_received

def send_name(client_socket, username, password, mode):
    payload = username + ":" + password + ":" + mode
    
    client_socket.sendall(payload.encode())

    res = client_socket.recv(1024)

    return res.decode()

def create_note(client_socket, note_title, note_content):
    client_socket.sendall(f"CREATE_NOTE:{note_title}:{note_content}".encode())
    print(f"\nNote created!\n")
    input("Press Enter to continue...")

def list_notes(client_socket):
    client_socket.sendall("LIST_NOTES".encode())
    data = client_socket.recv(1024)
    print(f"\nYour Notes:\n{data.decode()}\n")

    if(data.decode() == "No notes."):
        input("Press Enter to continue...")
        return -1
     
    return 0

def list_note(client_socket, note_id):
    client_socket.sendall(f"LIST_NOTE:{note_id}".encode())
    note = client_socket.recv(1024).decode()
    print(note)
    input("Press Enter to continue...")


def delete_note(client_socket, note_index):
    client_socket.sendall(f"DELETE_NOTE:{note_index}".encode())
    print(f"\nNote deleted successfully\n")
    input("Press Enter to continue...")