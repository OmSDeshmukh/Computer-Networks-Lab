import socket
import sys
import json
import random

def handle_client(connection, server_name):
    # receive data
    data = connection.recv(1024)
    if data:
        received_list = json.loads(data.decode())
        if received_list[1] > 100 or received_list[1] < 1:
            print("Server Closing")
            return 11

        print(f"Client Name: {received_list[0]}")
        print(f"Server Name: {server_name}")

        random_number = random.randint(1, 100)

        print(f"Client's random number: {received_list[1]}")
        total_sum = received_list[1] + random_number
        print(f"Sum of random numbers is {total_sum}")

        print(f"Server's random number: {random_number}")
        print('sending data back to the client')
        data_list = json.dumps([server_name, random_number])
        data = data_list.encode()
        connection.sendall(data)
    else:
        print("No data received")
        return 11

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10001)
server_name = "210010033_server"

print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)
print('waiting for a connection')
connection, client_address = sock.accept()
print("Client connected")
try:
    while True:
        # Wait for a connection
        if(handle_client(connection, server_name)==11):
            break
except KeyboardInterrupt:
    print("Server shutting down")
finally:
    sock.close()