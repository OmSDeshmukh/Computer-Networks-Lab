import socket
import sys
import random
import json
import threading
from key_generation import generate_rsa_key_pair
import time

client_details = dict()

def receive_updates_from_server(sock):
    while True:
        try:
            data = sock.recv(65536)
            updated_client_details = json.loads(data.decode())
        
            if(updated_client_details["identifier"]=="broadcast_message"):
                print("Received updated client details:", updated_client_details["data"])
                client_details = updated_client_details["data"]
            elif(updated_client_details["identifier"]=="Disconnection"):
                print("Disconnected from server")
                break
            elif(updated_client_details["identifier"]=="AFK"):
                name = updated_client_details["name"]
                client_details = updated_client_details["data"]
                print(f"{name} Left the chat")
        except Exception as e:
            print("Error receiving data from server:", e)
            break
        
        
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(f"Connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)

# Start a thread to receive updates from the server
receive_thread = threading.Thread(target=receive_updates_from_server, args=(sock,))

try:
    # Send the client's name
    client_name = input("Enter your name: ")
    sock.sendall(client_name.encode())
    print("Name sent")
    
    # Generate public and private keys for the client
    private_key, public_key = generate_rsa_key_pair()
    
    # Send the public key to the server
    sock.sendall(public_key)
    print("Public key sent")
    
    receive_thread.start()
    
    # choice = input("Enter the client you want to talk to")
    # print("Here are the names")
    # print(client_details.keys())
    
    i = int(input("Enter one to disconnect"))
    if i==1:
        sock.sendall("QUIT".encode())
        receive_thread.join()
        sock.close()

    # Wait for threads to complete
    # send_thread.join()
    # receive_thread.join()
except Exception as e:
    print("Error:", e)
finally:
    print('Closing socket')
    sock.close()
