import xmlrpc.client

class Client:
    def __init__(self, server_address):
        self.server = xmlrpc.client.ServerProxy(server_address)

    def add_note(self, note):
        return self.server.add_note(note)

    def get_note(self, id):
        return self.server.get_note(id)

    def view_all_notes(self):
        return self.server.view_all_notes()

    def delete_note(self, id):
        return self.server.delete_note(id)

def run_client(server_address):
    client = Client(server_address)

    while True:
        show_menu()
        choice = input("Please choose an option: ")
        handle_action(client, choice[0])

def show_menu():
    print('\nWelcome! Available actions:')
    print('1. Add note')
    print('2. View specific note')
    print('3. List all notes')
    print('4. Delete note')

def handle_action(client, choice):
    if choice == '1':
        note = input("Enter new note: ")
        result = client.add_note(note)
        print(result)
    elif choice == '2':
        note_id = input("Enter note id: ")
        result = client.get_note(note_id)
        print(result)
    elif choice == '3':
        result = client.view_all_notes()
        print(result)
    elif choice == '4':
        note_id = input("Enter note id: ")
        result = client.delete_note(note_id)
        print(result)
    else:
        print('Incorrect action')