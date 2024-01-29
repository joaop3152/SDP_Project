#Load Balancer - Round Robin
import socket
import threading
from Application.network import *

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_server = 0
        self.lock = threading.Lock()

    def get_next_server(self):
        with self.lock:
            server = self.servers[self.current_server]
            self.current_server = (self.current_server + 1) % len(self.servers)
        return server

    def start(self, lb_host, lb_port):
        lb_socket = create_socket()
        bind_socket(lb_socket, lb_host, lb_port)
        listen(lb_socket)
        print(f"Load Balancer ready to receive connections on {lb_host}:{lb_port}...")

        while True:
            conn, addr = lb_socket.accept()
            target_server = self.get_next_server()
            self.forward_request(conn, target_server)

    def forward_request(self, conn, target_server):
        with socket.create_connection(target_server) as server_conn:
            print(f"Forwarding request to {target_server}")
            
            print("\nÀ espera do cliente...")
            data = conn.recv(1024)

            print("\nRecebido. A enviar para o server...")
            server_conn.sendall(data)

            print("\nEnviado. À espera da resposta do server...")
            data = server_conn.recv(1024)

            print("\nRecebido. A enviar para o cliente...")
            conn.sendall(data)

            print("\nEnviado.")

if __name__ == "__main__":
    # Define your server addresses here
    server_addresses = [("127.0.0.1", 8888), ("127.0.0.1", 8889)]

    # Create and start the load balancer
    load_balancer = LoadBalancer(server_addresses)
    load_balancer.start("127.0.0.1", 8887)