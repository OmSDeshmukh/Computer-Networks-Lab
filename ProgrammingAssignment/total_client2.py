# client with everything handled
import socket
import sys
import random
import json
import threading
import base64
import cv2
import numpy as np
import struct
from key_generation import generate_rsa_key_pair
from key_generation import encrypt_string
from key_generation import decrypt_string

global client_details
client_details = dict()
lock = threading.Lock()

MESSAGE_TYPE_JSON = 1
MESSAGE_TYPE_FRAME = 2
buffer = []

# def is_json(data):
#     try:
#         json.loads(data)
#         return True
#     except json.JSONDecodeError:
#         return False
    
def pack_message(message_type, message_data):
     # Construct the message with header
    if(message_type == MESSAGE_TYPE_FRAME):
        header = struct.pack("!BI", message_type, len(message_data))
        message = header + message_data
    elif(message_type == MESSAGE_TYPE_JSON):
        header = struct.pack("!BI", message_type, len(message_data))
        message = header + message_data.encode()
    return message

def receive_updates_from_server(sock):
    global client_details
    # with lock:
    while True:
        try:
            header = sock.recv(5)
            try:
                message_type, message_size = struct.unpack("!BI", header)
                if(message_type==MESSAGE_TYPE_JSON):
                    json_data = sock.recv(message_size).decode()
                    updated_client_details = json.loads(json_data)
                    # updated_client_details = json.loads(data.decode())
                
                    if(updated_client_details["identifier"]=="broadcast_message"):
                        print("Received updated client details \n")
                        # with lock: #gimini
                        client_details = updated_client_details["data"]
                        
                    elif(updated_client_details["identifier"]=="Disconnection"):
                        print("Disconnected from server\n")
                        break
                    
                    elif(updated_client_details["identifier"]=="AFK"):
                        name = updated_client_details["name"]
                        # with lock:
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
                    
                    elif(updated_client_details["identifier"]=="Video List"):
                        video_list = updated_client_details["data"]
                        print("Availaible Videos")
                        for video in video_list:
                            for quality in video:
                                print(quality)
                            print("")
                    
                    elif(updated_client_details["identifier"]=="Video Frame"):
                        print("Video Streaming mode")
                        client_socket = sock
                        while True:
                            # For each of the frame
                            header = client_socket.recv(5)
                            try:
                                message_type, message_size = struct.unpack("!BI", header)
                                # Receive frame size
                                if(message_type == MESSAGE_TYPE_FRAME):
                                    frame_size_data = client_socket.recv(16)
                                    if not frame_size_data:
                                        break
                                    
                                    # handle case when final frame is sent
                                    # type error occurs here
                                    frame_size = int(frame_size_data.strip())
                                    if frame_size == 0:
                                        break

                                    # Receive frame data
                                    frame_data = b''
                                    while len(frame_data) < frame_size:
                                        remaining_bytes = frame_size - len(frame_data)
                                        data_recv = client_socket.recv(remaining_bytes)
                                        frame_data += data_recv
                                            

                                    # Convert frame data to numpy array
                                    frame_np = np.frombuffer(frame_data, dtype=np.uint8)

                                    # Decode frame
                                    frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)

                                    # Resize frame to 1280x720
                                    frame = cv2.resize(frame, (1280, 720))

                                    # Display frame
                                    # cv2.imshow('Video Stream', frame) # Not working on Mac
                                    
                                    if cv2.waitKey(1) & 0xFF == ord('q'):
                                        break
                                else:
                                    json_data = client_socket.recv(message_size).decode()
                                    message = json.loads(json_data)
                                    buffer.append(message)
                            except:
                                print("nothing received")
                                break
                        cv2.destroyAllWindows()
                        print("Stream finished")
            except:
                pass
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
                message = pack_message(MESSAGE_TYPE_JSON,data_json)
                sock.sendall(message)
            else:
                print("Incorrect Name Please enter again\n")
                
        if(choice == 2):
            data = {
                "identifier" : "Video List",
            }
            data_json = json.dumps(data)
            message = pack_message(MESSAGE_TYPE_JSON,data_json)
            sock.sendall(message)
            
            choice = input("Enter video name (as Video1_240p):")
            data = {
                "identifier" : "Video Choice",
                "choice" : choice,
                "from" : client_name
            }
            data_json = json.dumps(data)
            message = pack_message(MESSAGE_TYPE_JSON,data_json)
            sock.sendall(message)
            print("Choice Sent")
            
        if(choice == 3):
            data = {
                "identifier":"QUIT"
            }
            data_json = json.dumps(data)
            message = pack_message(MESSAGE_TYPE_JSON,data_json)
            sock.sendall(message)
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