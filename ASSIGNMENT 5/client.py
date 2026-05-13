import socket
import threading

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024


class TokenRingClient:

    def __init__(self):

        self.client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.has_token = False

        self.running = True

    # Receive messages
    def receive_messages(self):

        while self.running:

            try:

                data = self.client_socket.recv(
                    BUFFER_SIZE
                ).decode()

                # Token received
                if data == "TOKEN":

                    self.has_token = True

                    print(
                        "\nTOKEN RECEIVED"
                    )

                # Release first
                elif data == "RELEASE_FIRST":

                    print(
                        "\nRelease token first"
                    )

                elif data == "TOKEN_REMOVED":

                    self.has_token = False

                    print(
                        "\nTOKEN MOVED TO NEXT CLIENT"
                    )

                # Server closed
                elif data == "SERVER_EXIT":

                    print("\nServer Closed")

                    self.has_token = False

                    self.running = False

                    try:
                        self.client_socket.close()
                    except:
                        pass

                    break

            except:

                self.running = False

                break

    def start(self):

        self.client_socket.connect((HOST, PORT))

        name = input("Enter Client Name: ")

        self.client_socket.send(name.encode())

        print("Connected to Server")

        thread = threading.Thread(
            target=self.receive_messages
        )

        thread.daemon = True
        thread.start()

        while True:

            if not self.running:
                break
            print("\n===== CLIENT MENU =====")
            print("1. Check Token")
            print("2. Release Token")
            print("3. Exit")

            choice = input("Enter Choice: ")

            # Check token
            if choice == "1":

                if self.has_token:

                    print(
                        "\nYou currently hold token"
                    )

                else:

                    print(
                        "\nYou do not have token"
                    )

            # Release token
            elif choice == "2":

                if self.has_token:

                    self.client_socket.send(
                        "RELEASE".encode()
                    )

                    self.has_token = False

                    print(
                        "\nToken Released"
                    )

                else:

                    print(
                        "\nYou don't hold token"
                    )

            # Exit
            elif choice == "3":

                # Server already closed
                if not self.running:

                    print("\nClient Closed")

                    break

                # Cannot exit with token
                if self.has_token:

                    print(
                        "\nRelease token first"
                    )

                else:

                    try:

                        self.client_socket.send(
                            "EXIT".encode()
                        )

                    except:
                        pass

                    print("\nExiting Client")

                    self.running = False

                    try:
                        self.client_socket.close()
                    except:
                        pass

                    break

            else:
                print("Invalid Choice")


if __name__ == "__main__":

    client = TokenRingClient()

    client.start()