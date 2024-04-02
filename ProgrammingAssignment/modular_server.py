import socket
import sys
import json
import threading

# Constants for message identifiers
class MessageTypes:
    BROADCAST = "broadcast_message"
    AFK = "AFK"
    COMMUNICATION = "Communication"
    QUIT = "QUIT"
    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('Server starting up on %s port %s' % server_address)
sock.bind(server_address)

# put socket in listening mode for TCP connections
sock.listen(5)

global client_details
client_details = dict() # name : public key
lock = threading.Lock()
client_socks = dict() # to store the socket : public key mapping

# best to calculate all the messages outside this function and use this only for braodcasting
def broadcast(message_json):
    global client_details,client_socks
    for client_socket in list(client_socks.keys()):
        try:
            # broadcast only to the other clients HANDLE ITTTTTT
            client_socket.sendall(message_json.encode())
        except:
            remove_client(client_socket)

def broadcast_dictionary():
    global client_details
    message = {
            "identifier": MessageTypes.BROADCAST,  # Use a suitable identifier value
            "data": client_details
        }
    message_json = json.dumps(message)
    broadcast(message_json)
    
def remove_client(client_socket):
    global client_details, client_socks
    with lock:
        temp = ""
        if client_socket in client_socks:
            public_key = client_socks[client_socket]
            for name, key in list(client_details.items()):
                if key == public_key:
                    temp = name
                    del client_details[name]
                    break
            del client_socks[client_socket]
            print("Removed client since it closed")
            message = {
                "identifier": MessageTypes.AFK,  # Use a suitable identifier value
                "data": client_details,
                "name": temp
            }
            message_json = json.dumps(message)
            broadcast(message_json)
                    
def send_to_single_client(connection, message_json):
    connection.sendall(message_json.encode())
    remove_client(connection)
    client_thread.interrupt()
    
def handle_message(connection, message_json):
    if(message_json["identifier"]==MessageTypes.QUIT):
        message = {
            "identifier": MessageTypes.QUIT  # Use a suitable identifier value
        }
        message_json = json.dumps(message)
        send_to_single_client(connection, message_json)
        # move this into the broadcast function
        
    if(message_json["identifier"]==MessageTypes.COMMUNICATION):
        print("Incoming message from: ",message_json["from"])
        broadcast(message_json)
    
    
def handle_client_connection(connection, client_address):
    try:
        name_received = connection.recv(1024).decode()
        print("Name received:", name_received)
        
        public_key_received = connection.recv(4096).decode()
        print("Public Key received:", public_key_received)
        
        # Adding client details into the dictionary (thread-safe)
        with lock:
            client_details[name_received] = public_key_received
            client_socks[connection] = public_key_received
            
        print("Current Client Details:", client_details)
        
        # Updating every client
        with lock:
            broadcast_dictionary()
            print("All Client Updated")
            
        while True:
            message = connection.recv(4096).decode()
            message_json = json.loads(message)
            handle_message(connection, message_json)
            

    except KeyboardInterrupt:
        print("Server interrupted. Closing connections.")
        connection.close()
        sys.exit(0)  # Exit the program gracefully
    except Exception as e:
        print(f"Connection closed by client {client_address}")
    finally:
        connection.close()

try:
    while True:
        # Accept incoming connections
        connection, client_address = sock.accept()
        print(f"Connected to client {client_address}")
        
        # Add the client socket to the list of clients
        client_socks[connection] = ""
        
        # Create a new thread to handle client connection
        client_thread = threading.Thread(target=handle_client_connection, args=(connection, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("Server interrupted. Closing.")
finally:
    sock.close()
