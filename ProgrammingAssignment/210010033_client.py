import socket
import sys
import random
import json
import threading
from key_generation import generate_rsa_key_pair

# client_name = "client7"

def receive_updates_from_server(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            updated_client_details = json.loads(data.decode())
            print("Received updated client details:", updated_client_details)
        except Exception as e:
            print("Error receiving data from server:", e)
            break
        
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(f"connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)

# Start a thread to receive updates from the server
receive_thread = threading.Thread(target=receive_updates_from_server, args=(sock,))

try:
    # while True:
    # When client connects, it will be asked for name and public key
    
    # sending the name
    welcome_string1 = sock.recv(1024).decode()
    if(welcome_string1 == "Enter your name: "):
        client_name = input("Enter your name: ")
        sock.sendall(client_name.encode())
        print("Name sent")
        
    # generate public and private keys for the client
    private_key, public_key = generate_rsa_key_pair()
    
    # sending the public key to the server
    welcome_string2 = sock.recv(1024).decode()
    if(welcome_string2 == "Enter the public key: "):
        sock.sendall(public_key)
        print("Public key sent")
        
    # receiving the client details dictionary from the server
    data = sock.recv(4096)
    client_details_dict = json.loads(data.decode())
    print("Other client details are as follows: ")
    print(client_details_dict)
except:
    print('Closing socket because server closed connection because integer sent by client was out of required range')
    sock.close()
    
print('closing socket')
sock.close()


# would need when dictionary size grows too much
# def send_dictionary_over_socket(sock, dictionary):
#     # Serialize the dictionary to JSON
#     data_json = json.dumps(dictionary)
    
#     # Calculate the size of the JSON data in bytes
#     data_size = len(data_json)
    
#     # Set the buffer size based on data size
#     buffer_size = max(1024, data_size)  # Minimum buffer size of 1024 bytes
    
#     # Send the data in chunks if it exceeds the buffer size
#     if data_size <= buffer_size:
#         sock.sendall(data_json.encode())
#     else:
#         for i in range(0, data_size, buffer_size):
#             chunk = data_json[i:i+buffer_size]
#             sock.sendall(chunk.encode())