import socket
import sys
import random
import json
from key_generation import generate_rsa_key_pair

client_name = "client1"

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10002)
print(f"connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)

try:
    while True:
        # When client connects, it will be asked for name and public key
        
        # sending the name
        welcome_string1 = sock.recv(1024).decode()
        if(welcome_string1 == "Enter your name: "):
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
        data = sock.recv(1024)
        client_details_dict = json.loads(data.decode())
        print("Other client details are as follows: ")
        print(client_details_dict)
        
        break
except:
    print('Closing socket because server closed connection because integer sent by client was out of required range')
    sock.close()
    
print('closing socket')
sock.close()