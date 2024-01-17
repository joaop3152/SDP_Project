import Client

def main():
    server_ip = input("Enter the server IP address: ")
    port = int(input("Enter port: "))
    server_address = f"http://{server_ip}:{port}"
    Client.run_client(server_address)


if __name__ == "__main__":
    main()


