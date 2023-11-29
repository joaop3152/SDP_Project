# server.py
import threading
from Application.network import create_socket, bind_socket, listen

def handle_client(client_socket, client_address, clients):
    print(f"Conexao estabelecida com {client_address}")
    client_name = client_socket.recv(1024).decode()
    clients[client_name] = client_socket

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
