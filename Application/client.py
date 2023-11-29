# client.py
from Application.network import create_socket

def connect_to_server(host, port):
    client_socket = create_socket()
    client_socket.connect((host, port))
    return client_socket

def send_name(client_socket, name):
    client_socket.sendall(name.encode())

def send_message(client_socket, target, message):
    client_socket.sendall(f"{target}:{message}".encode())

def receive_message(client_socket):
    data = client_socket.recv(1024)
    return data.decode()
