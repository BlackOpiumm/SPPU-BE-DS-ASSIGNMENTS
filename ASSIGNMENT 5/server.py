import socket
import threading
import time

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024


class TokenRingServer:

    def __init__(self):

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server_socket.bind((HOST, PORT))

        self.server_socket.listen()

        self.clients = []
        self.client_names = []

        self.current_token_index = -1

        self.running = True

    # Add clients
    def add_clients(self):

        count = int(
            input("\nEnter Number of Clients: ")
        )

        print("\nWaiting for clients...\n")

        for _ in range(count):

            client_socket, address = \
                self.server_socket.accept()

            name = client_socket.recv(
                BUFFER_SIZE
            ).decode()

            self.clients.append(client_socket)
            self.client_names.append(name)

            print(f"{name} connected")

            # Thread for client
            thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, name)
            )

            thread.daemon = True
            thread.start()

    # Handle client
    def handle_client(self, client_socket, name):

        while self.running:

            try:

                data = client_socket.recv(
                    BUFFER_SIZE
                ).decode()

                # Token released
                if data == "RELEASE":

                    print(
                        f"\n{name} released token"
                    )

                    self.pass_token()

                # Client exit
                elif data == "EXIT":

                    index = self.client_names.index(
                        name
                    )

                    # Cannot exit while holding token
                    if index == self.current_token_index:

                        client_socket.send(
                            "RELEASE_FIRST".encode()
                        )

                    else:

                        self.remove_client(name)

                        break

            except:
                break

    def pass_token(self):

        if len(self.clients) == 0:
            return

        # Remove token from previous holder
        if self.current_token_index != -1:

            try:

                old_client = self.clients[
                    self.current_token_index
                ]

                old_client.send(
                    "TOKEN_REMOVED".encode()
                )

            except:
                pass

        # Move token in ring
        self.current_token_index = \
            (self.current_token_index + 1) \
            % len(self.clients)

        # Give token to next client
        client_socket = self.clients[
            self.current_token_index
        ]

        client_socket.send("TOKEN".encode())

        print(
            f"\nTOKEN moved to "
            f"{self.client_names[self.current_token_index]}"
        )

    # Remove client
    def remove_client(self, name):

        if name in self.client_names:

            index = self.client_names.index(name)

            self.clients[index].close()

            del self.clients[index]
            del self.client_names[index]

            print(f"\n{name} removed")

            # Adjust token index
            if len(self.clients) > 0:

                self.current_token_index %= \
                    len(self.clients)

            else:

                self.current_token_index = -1

    # Ring structure
    def show_ring(self):

        if len(self.client_names) == 0:

            print("\nNo clients in ring")
            return

        ring = " -> ".join(self.client_names)

        ring += f" -> {self.client_names[0]}"

        print(f"\nRing Structure:\n{ring}")

    # Menu
    def start(self):

        print("\n===== TOKEN RING SERVER =====")

        self.add_clients()

        # Start token initially
        self.pass_token()

        while self.running:

            print("\n===== SERVER MENU =====")
            print("1. Show Ring")
            print("2. Current Token Holder")
            print("3. Add Clients")
            print("4. Pass Token")
            print("5. Exit")

            choice = input("Enter Choice: ")

            # Ring
            if choice == "1":

                self.show_ring()

            # Current holder
            elif choice == "2":

                if self.current_token_index == -1:

                    print(
                        "\nNo token holder"
                    )

                else:

                    print(
                        f"\nCurrent Token Holder: "
                        f"{self.client_names[self.current_token_index]}"
                    )

            # Add clients
            elif choice == "3":

                self.add_clients()

            # Pass token manually
            elif choice == "4":

                self.pass_token()

            # Exit
            elif choice == "5":

                print("\nClosing Server")

                for client in self.clients:

                    try:
                        client.send(
                            "SERVER_EXIT".encode()
                        )

                        client.close()

                    except:
                        pass

                self.running = False

                self.server_socket.close()

                break

            else:
                print("Invalid Choice")


if __name__ == "__main__":

    server = TokenRingServer()

    server.start()