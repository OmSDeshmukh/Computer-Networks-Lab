import socket
import sys
import json
import random    

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10002)
server_name = socket.gethostname()

print(' Server starting up on %s port %s' % server_address)
sock.bind(server_address)

# put socket in listening mode for TCP connections
# Listen for incoming connections
sock.listen(5)
# print('waiting for a connection')

client_details = dict()

while True:
    # connecting to the client
    connection, client_address = sock.accept()
    print("Client connected")
    
    try:
    # Wait for a connection
        while True:
            welcome_string1 = "Enter your name: "
            connection.sendall(welcome_string1.encode())
            name_received = connection.recv(1024).decode()
            print("Name received")
            
            welcome_string2 = "Enter the public key: "
            connection.sendall(welcome_string2.encode())
            public_key_received = connection.recv(1024).decode()
            print("Public Key received")
            
            # adding client details into the dictionary
            client_details[name_received] = public_key_received
            
            print(client_details)
            # Sending the dictionary to the client 
            client_details_json = json.dumps(client_details)
            connection.sendall(client_details_json.encode())
            print("All Client Details sent")

    except Exception as e:
        print("Connection closed by client")
        break
    finally:
        connection.close()
    
print("Server Closing")
connection.close()
sock.close()