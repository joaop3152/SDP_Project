# run_client.py
import sys
from Application.client import *

SERVER_IP = '127.0.0.1'
PORT = 8888

def show_authenticated_menu(username):
    print(f"--- Menu - Note Taking - Welcome {username} ---")
    print("1. Create a new note")
    print("2. My notes")
    print("3. Delete note")
    print("0. Exit")

def main():
    try:
        client_socket = connect_to_server(SERVER_IP, PORT)
    except:
        print("Something went wrong with the connection.")
        sys.exit()


    # maybe create a better way to authenticate user !
    print("Welcome to Note Taking!\n")
    print("--- Please authenticate ---")
    username = input("Username: ")
    password = input("Password: ")
    send_name(client_socket, username, password)

    # NOTE: server commands only work with the client authenticated 

    # Main loop (enters loop with client already authenticated)
    while True:
        show_authenticated_menu(username)

        choice = input("Please choose an option: ")

        if choice == "1":
            note_content = input("Start writing: ")
            create_note(client_socket, note_content)

        elif choice == "2":
            list_notes(client_socket)

        elif choice == "3":
            note_index = input("Index of note to be erased: ")
            delete_note(client_socket, note_index)

        elif choice == "0":
            print("Closing client.\n Thank you for using Note Taking!")
            client_socket.close()
            break
        else:
            print("Wrong option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Forced exit. Goodbye!")
    finally:
        sys.exit()