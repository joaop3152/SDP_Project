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

        if choice == "1": #Create note # TODO: create the option to save a title and then the note. When displayed, shows only the title.
            utils.clear_console()
            note_content = input("\nStart writing: \n")
            create_note(client_socket, note_content)

        elif choice == "2": #List all notes of the authenticated user # TODO: List all notes by the title, and then give the option to open an note indicated by the index
            utils.clear_console()
            list_notes(client_socket)

        elif choice == "3": #Delete a note according an given index
            utils.clear_console()
            list_notes_to_erase(client_socket)
            note_index = input("\nIndex of note to be erased: ")
            delete_note(client_socket, note_index)

        elif choice == "0": #Close connection and exit application
            utils.clear_console()
            print("\nClosing client.\n Thank you for using Note Taking!\n")
            client_socket.close()
            break
        else: # Wrong input
            print("\nWrong option. Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Forced exit. Goodbye!")
    finally:
        sys.exit()