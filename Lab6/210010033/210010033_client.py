import socket
import sys
import random
import json

client_name = "210010033_client"

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(f"connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)

try:
    while True:
        # Send data
        random_number = random.randint(1, 100)
        data_list = json.dumps([client_name, random_number])
        data = data_list.encode()
        sock.sendall(data)
        # print("data sent")

        data = sock.recv(1024)

        received_list = json.loads(data.decode())
        # if received_list[1] > 100 or received_list[1] < 1:
        #     print("Integer sent by server is out of range")
        #     print("Closing connection and switching client off")
        #     break  # Exit the loop if integer is out of range
        # else:
        print(f"Server Name: {received_list[0]}")
        print(f"Random number from server: {received_list[1]}")
        i = int(input("Press 1 to continue sending messages\nPress 0 to stop sending messages and close client and server"))
        if i == 0:
            break  # Exit the loop if user chooses to stop sending messages
except:
    print('Closing socket because server closed connection because integer sent by client was out of required range')
    sock.close()
    
print('closing socket')
sock.close()