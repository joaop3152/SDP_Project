import Server

def main():
    server_ip = input("Enter the server IP address: ")
    port = int(input("Enter port: "))
    Server.run_server(server_ip, port)

if __name__ == "__main__":
    main()
