# run_client.py
import sys
import Application.utilities as utils
from Application.client import *

APP_TITLE = "Note Taking"
SERVER_IP = '127.0.0.1'
PORT = 8888

def show_authenticated_menu(username):
    utils.clear_console()
    print(f"\n--- Menu - {APP_TITLE} - Welcome {username} ---\n")
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
    print(f"\nWelcome to {APP_TITLE}!\n")
    print("--- Please authenticate ---")
    username = input("Username: ")
    password = input("Password: ")
    send_name(client_socket, username, password)

    # NOTE: server commands only work with the client authenticated 

    # Main loop (enters loop with client already authenticated)
    while True:
        show_authenticated_menu(username)

        choice = input("\nPlease choose an option: ")

        if choice == "1":
            utils.clear_console()
            note_content = input("\nStart writing: \n")
            create_note(client_socket, note_content)

        elif choice == "2":
            utils.clear_console()
            list_notes(client_socket)

        elif choice == "3":
            utils.clear_console()
            list_notes_to_erase(client_socket)
            note_index = input("\nIndex of note to be erased: ")
            delete_note(client_socket, note_index)

        elif choice == "0":
            utils.clear_console()
            print("\nClosing client.\n Thank you for using Note Taking!\n")
            client_socket.close()
            break
        else:
            print("\nWrong option. Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Forced exit. Goodbye!")
    finally:
        sys.exit()