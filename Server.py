import xmlrpc.server


class Server:
    def __init__(self):
        self.clients = []

    def add_note(self, note):
        print(f"Note added: {note}")
        return f"Note added: {note}"

    def get_note(self, id):
        print(f"Note with id: {id}")
        return f"Note with id: {id}"

    def view_all_notes(self):
        print('List notes')
        return "List notes"

    def delete_note(self, id):
        print(f"Deleted note with id {id}")
        return f"Deleted note with id {id}"

def run_server(server_ip, port):
    server = xmlrpc.server.SimpleXMLRPCServer((server_ip, port), allow_none=True)
    server.register_instance(Server())

    print(f"Server running at address {server_ip}:{port}...")
    server.serve_forever()
