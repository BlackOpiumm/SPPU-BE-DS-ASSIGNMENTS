import socket
import time
import json
import random
from datetime import datetime

SERVER_IP = "127.0.0.1"
PORT = 5000


def get_client_time():

    # Current system time
    current_time = time.time()

    # Random offset of few seconds/minutes
    offset = random.randint(-300, 300)

    return current_time + offset


def format_time(timestamp):

    return datetime.fromtimestamp(timestamp).strftime(
        "%H:%M:%S"
    )


def main():

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client_socket.connect((SERVER_IP, PORT))

    print(f"Connected to {SERVER_IP}:{PORT}")

    client_time = get_client_time()

    adjusted = False

    while not adjusted:

        server_res = json.loads(
            client_socket.recv(1024).decode()
        )

        # Send local time
        if server_res["operation"] == "time_req":

            print(f"\nClient Local Time : "
                  f"{format_time(client_time)}")

            client_socket.send(
                json.dumps({
                    "client_time": client_time
                }).encode()
            )

        # Receive adjustment
        elif server_res["operation"] == "time_adj":

            print(f"\nTime Adjustment : "
                  f"{server_res['adjustment']:.2f} seconds")

            client_time += float(
                server_res["adjustment"]
            )

            print(f"Adjusted Time : "
                  f"{format_time(client_time)}")

            adjusted = True

    client_socket.close()


if __name__ == "__main__":
    main()