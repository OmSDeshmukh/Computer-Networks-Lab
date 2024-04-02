import socket
import sys
import random
import json
import threading
from key_generation import generate_rsa_key_pair
from key_generation import encrypt_string
from key_generation import decrypt_string
import time
import base64

global client_details
client_details = dict()
lock = threading.Lock()

def receive_updates_from_server(sock):
    global client_details
    # with lock:
    while True:
        try:
            data = sock.recv(65536)
            updated_client_details = json.loads(data.decode())
        
            if(updated_client_details["identifier"]=="broadcast_message"):
                print("Received updated client details \n")
                client_details = updated_client_details["data"]
                
            elif(updated_client_details["identifier"]=="Disconnection"):
                print("Disconnected from server\n")
                break
            
            elif(updated_client_details["identifier"]=="AFK"):
                name = updated_client_details["name"]
                client_details = updated_client_details["data"]
                print(f"{name} Left the chat\n")
                print("Received updated client details \n")
                
            elif(updated_client_details["identifier"]=="Communication"):
                encrypt_message_base64_r = updated_client_details["encrypt_message"]
                encrypt_message_r = base64.b64decode(encrypt_message_base64_r)
                try:
                    decrpyted_message = decrypt_string(encrypt_message_r, private_key)
                    print("Message received from: ",updated_client_details["from"])
                    print("Message: ", decrpyted_message)
                except:
                    print("Message not for us!\n")
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
    
    while True:
        # Printing Choices
        choice = int(input("Enter \n 1 to Talk to client \n 2 to Stream Video \n 3 to QUIT \n"))
        
        if(choice == 1):
            print("Here are the names")
            # with lock:
            print(client_details.keys())
            name = input("Enter the client you want to talk to: \n")
            if(name in list(client_details.keys())):
                # taking the client details you want to connect to
                pk = client_details[name]
                
                message = input("Enter the message you want to send to the client\n")
                encrypt_message = encrypt_string(message,pk)
                encrypt_message_base64 = base64.b64encode(encrypt_message).decode()
                data = {
                    "identifier" : "Communication",
                    "encrypt_message" : encrypt_message_base64,
                    "from": client_name
                }
                data_json = json.dumps(data)
                sock.sendall(data_json.encode())
            else:
                print("Incorrect Name Please enter again\n")
                
        if(choice == 2):
            pass
        
        if(choice == 3):
            data = {
                "identifier":"QUIT"
            }
            data_json = json.dumps(data)
            sock.sendall(data_json.encode())
            receive_thread.join()
            sock.close()
            break

    # Wait for threads to complete
    # send_thread.join()
    # receive_thread.join()
except Exception as e:
    print("Error:", e)
finally:
    print('Closing socket')
    sock.close()
