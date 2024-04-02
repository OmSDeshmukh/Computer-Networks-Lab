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

global client_details
client_details = dict() # name : public key
lock = threading.Lock()
# clients = []  # List to store connected client sockets
client_socks = dict() # to store the socket : public key mapping

# best to calculate all the messages outside this function and use this only for braodcasting
def broadcast_dictionary(*args):
    global client_details
    if(len(args)==0):
        message = {
            "identifier": "broadcast_message",  # Use a suitable identifier value
            "data": client_details
        }
    elif(len(args)==1):
        message = {
            "identifier": "AFK",  # Use a suitable identifier value
            "data": client_details,
            "name": args[0]
        }
    elif(len(args)==2):
        message = {
            "identifier" : "Communication",
            "encrypt_message" : args[0],
            "from" : args[1]
        }
    updated_client_details_json = json.dumps(message)
    for client_socket in list(client_socks.keys()):
        try:
            # broadcast only to the other clients HANDLE ITTTTTT
            client_socket.sendall(updated_client_details_json.encode())
        except:
            remove_client(client_socket)


def remove_client(client_socket):
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
            broadcast_dictionary(temp)
            
# def handle_message_received()
                    

def handle_client_connection(connection, client_address):
    try:
        # while True:
        # welcome_string1 = "Enter your name: "
        # connection.sendall(welcome_string1.encode())
        name_received = connection.recv(1024).decode()
        print("Name received:", name_received)
        
        # welcome_string2 = "Enter the public key: "
        # connection.sendall(welcome_string2.encode())
        public_key_received = connection.recv(4096).decode()
        print("Public Key received:", public_key_received)
        
        # Adding client details into the dictionary (thread-safe)
        with lock:
            client_details[name_received] = public_key_received
            client_socks[connection] = public_key_received
            
        print("Current Client Details:", client_details)
        
        # Sending the updated dictionary to the client 
        # Updating every client
        with lock:
            broadcast_dictionary()
            print("All Client Updated")
            
        while True:
            message = connection.recv(4096).decode()
            message_json = json.loads(message)
            if(message_json["identifier"]=="QUIT"):
                # move this into the broadcast function
                message = {
                    "identifier": "Disconnection"  # Use a suitable identifier value
                }
                connection.sendall(json.dumps(message).encode())
                remove_client(connection)
                client_thread.interrupt()
            if(message_json["identifier"]=="Communication"):
                print("Incoming message from: ",message_json["from"])
                broadcast_dictionary(message_json["encrypt_message"],message_json["from"])
                # pass
            

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
