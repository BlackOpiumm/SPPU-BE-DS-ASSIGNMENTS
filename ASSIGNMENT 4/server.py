import socket
import time
import json
from datetime import datetime

SERVER_IP = "127.0.0.1"
PORT = 5000


def get_system_time():
    return time.time()


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime(
        "%H:%M:%S"
    )


def main():

    # Create server socket
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.bind((SERVER_IP, PORT))
    server_socket.listen(5)

    # Actual server system time
    server_time = get_system_time()

    print(f"\nTime Server Running on {SERVER_IP}:{PORT}")
    print(f"Server Time : {format_time(server_time)}\n")

    clients = []

    while True:

        client_socket, client_address = server_socket.accept()

        print(f"Connected with {client_address}")

        clients.append(client_socket)

        option = input(
            "\nAdd more clients? (y/n): "
        )

        if option.lower() == "n":
            break

    client_times = []

    # Request client times
    for client_socket in clients:

        request = json.dumps({
            "operation": "time_req"
        })

        client_socket.send(request.encode())

        response = json.loads(
            client_socket.recv(1024).decode()
        )

        client_time = float(response["client_time"])

        client_times.append(client_time)

    # Berkeley Algorithm
    total_time = server_time + sum(client_times)

    average_time = total_time / (len(client_times) + 1)

    print("\n========= TIME SYNCHRONIZATION =========")

    print(f"\nServer Original Time : "
          f"{format_time(server_time)}")

    for i, ct in enumerate(client_times):

        print(f"Client {i+1} Original Time : "
              f"{format_time(ct)}")

    print(f"\nAverage Time : "
          f"{format_time(average_time)}\n")

    # Send adjustment to clients
    for i, client_socket in enumerate(clients):

        adjustment = average_time - client_times[i]

        response = json.dumps({
            "operation": "time_adj",
            "adjustment": adjustment
        })

        client_socket.send(response.encode())

        print(f"Adjustment sent to Client {i+1}")

    server_socket.close()


if __name__ == "__main__":
    main()