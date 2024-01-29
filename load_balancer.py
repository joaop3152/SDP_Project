import socket
import threading

# Define a list of values to be sent to clients
data_list = [8888, 8889]
current_index = 0

def handle_client(client_socket):
    global current_index
    
    # Get the value from the list based on the current index
    data_to_send = data_list[current_index]
    
    # Increment the index for the next connection
    current_index = (current_index + 1) % len(data_list)

    # Send the value to the client
    client_socket.sendall(str(data_to_send).encode('utf-8'))
    print("sent " + str(data_to_send))
    
    # Close the connection
    client_socket.close()

def start_server(port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('localhost', port))

    # Listen for incoming connections
    server_socket.listen()
    print(f"Server listening on port {port}...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    # Set the port you want the server to listen on
    port_number = 8887
    start_server(port_number)
