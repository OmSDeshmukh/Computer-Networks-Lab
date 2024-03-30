import socket
import sys
import json
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('Server starting up on %s port %s' % server_address)
sock.bind(server_address)

# put socket in listening mode for TCP connections
sock.listen(5)

client_details = dict()
lock = threading.Lock()
clients = []  # List to store connected client sockets

def broadcast_dictionary():
    while True:
        updated_client_details_json = json.dumps(client_details)
        for client_socket in clients:
            try:
                client_socket.sendall(updated_client_details_json.encode())
            except:
                # Handle any exceptions if the client connection is closed
                clients.remove(client_socket)
                

def handle_client_connection(connection, client_address):
    try:
        while True:
            welcome_string1 = "Enter your name: "
            connection.sendall(welcome_string1.encode())
            name_received = connection.recv(1024).decode()
            print("Name received:", name_received)
            
            welcome_string2 = "Enter the public key: "
            connection.sendall(welcome_string2.encode())
            public_key_received = connection.recv(1024).decode()
            print("Public Key received:", public_key_received)
            
            # Adding client details into the dictionary (thread-safe)
            with lock:
                client_details[name_received] = public_key_received
                
            print("Current Client Details:", client_details)
            
            # Sending the updated dictionary to the client 
            with lock:
                client_details_json = json.dumps(client_details)
            connection.sendall(client_details_json.encode())
            print("All Client Details sent")
            
            # with lock:
            #     broadcast_thread = threading.Thread(target=broadcast_dictionary)
            #     broadcast_thread.start()
            #     broadcast_thread.join()
            #     print("Client Details Broadcasted")

    except KeyboardInterrupt:
        print("Server interrupted. Closing connections.")
        connection.close()
        sys.exit(0)  # Exit the program gracefully
    except Exception as e:
        print(f"Connection closed by client {client_address}")
    finally:
        connection.close()

# Start the broadcast thread
broadcast_thread = threading.Thread(target=broadcast_dictionary)
# broadcast_thread.start()

try:
    while True:
        # Accept incoming connections
        connection, client_address = sock.accept()
        print(f"Connected to client {client_address}")
        
        # Add the client socket to the list of clients
        clients.append(connection)
        
        # Create a new thread to handle client connection
        client_thread = threading.Thread(target=handle_client_connection, args=(connection, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("Server interrupted. Closing.")
finally:
    sock.close()
