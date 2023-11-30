# run_client.py
from Application.client import connect_to_server, send_name, send_message, receive_message

SERVER_IP = 'SERVER_IP_ADDRESS'
PORT = 12345

client_socket = connect_to_server(SERVER_IP, PORT)

name = input("Enter your name: ")
send_name(client_socket, name)

while True:
    target = input("Send message to: ")
    message = input(f"Enter your message for {target}: ")
    send_message(client_socket, target, message)
    data = receive_message(client_socket)
    print(f"Received: {data}")

client_socket.close()