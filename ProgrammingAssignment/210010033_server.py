import socket
import sys
import json
import threading
import cv2
import struct
import os

# Define message types
MESSAGE_TYPE_JSON = 1
MESSAGE_TYPE_FRAME = 2

global client_details
client_details = dict() # name : public key mapping
lock = threading.Lock()
client_socks = dict() #  socket : public key mapping

# This part is to handle the video file
def list_video_files():
    VIDEO_DIR = "videos/"
    video_files = []  

    for f in os.listdir(VIDEO_DIR):
        if(f.endswith('.mp4')):
            video_files.append(f)
    return video_files

# for packing message with its identifier
def pack_message(message_type, message_data):
     # Construct the message with header
    if(message_type == MESSAGE_TYPE_FRAME):
        header = struct.pack("!BI", message_type, len(message_data))
        message = header + message_data
    elif(message_type == MESSAGE_TYPE_JSON):
        header = struct.pack("!BI", message_type, len(message_data))
        message = header + message_data.encode()
    return message

            
# Function to broadcast messages to all the clients
def broadcast(message):
    global client_details, client_socks
    updated_client_details_json = json.dumps(message)
    updated_client_details_message = pack_message(MESSAGE_TYPE_JSON,updated_client_details_json)
    for client_socket in list(client_socks.keys()):
        try:
            client_socket.sendall(updated_client_details_message)
        except:
            remove_client(client_socket)


# Function to stream video to a specific client connection
def stream_video(connection, choice):
    videos = []
    videos.append(f"videos/{choice}_240p.mp4")
    videos.append(f"videos/{choice}_720p.mp4")
    videos.append(f"videos/{choice}_1440p.mp4")
    # frame_counts = [0] * len(videos)
    current_file_index = 0
    while current_file_index < len(videos):
        cap = cv2.VideoCapture(videos[current_file_index])
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = (total_frames // 3)*current_file_index
        end_frame = (total_frames // 3) * (current_file_index+1)
        
        print("file_name: ",videos[current_file_index])
        print("start_frame: ", start_frame, " end_frame: ", end_frame, "total_frames: ", total_frames)
        
        # for each frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            # Serialize frame
            frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
            
            # Send frame size and data
            message = pack_message(MESSAGE_TYPE_FRAME,(str(len(frame_data))).encode().ljust(16) + frame_data)
            connection.sendall(message)
            
            # print("Frame sent")
            # Switch to the next file if one-third of frames sent
            if  current_frame >= end_frame:
                current_file_index += 1
                break
        
        cap.release()
    print("Stream Finished")

    # to aknowledge that streaming has finished
    message = {
        "identifier": "Video Finish"
    }
    message_json = json.dumps(message)
    message = pack_message(MESSAGE_TYPE_JSON,message_json)
    connection.sendall(message)

# Function to remove a client connection when it quits and broadcast it to all the clients
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
            print(f"Removed client {temp} since it quit")
            message = {
                "identifier": "AFK",  
                "data": client_details,
                "name": temp
            }
            broadcast(message)
                    

# Function to handle the client connection
def handle_client_connection(connection, client_address):
    global client_details, client_socks
    try:
        welcome_string1 = "Enter your name: "
        connection.sendall(welcome_string1.encode())
        name_received = connection.recv(1024).decode()
        print("Name received:", name_received)
        
        welcome_string2 = "Enter the public key: "
        connection.sendall(welcome_string2.encode())
        public_key_received = connection.recv(4096).decode()
        print(f"Public Key received from {name_received}")
        
        # Adding client details into the dictionary (thread-safe)
        with lock:
            client_details[name_received] = public_key_received
            client_socks[connection] = public_key_received
            
        # print("Current Client Details:", client_details)
        
        
        # Updating every client
        with lock:
            message = {
                "identifier": "broadcast_message",  
                "data": client_details,
                "name" : name_received
            }
            broadcast(message)
            print("All Client Updated")
            
        while True:
            header = connection.recv(5)
            try:
                message_type, message_size = struct.unpack("!BI", header)
                if(message_type == MESSAGE_TYPE_JSON):
                    json_data = connection.recv(message_size).decode()
                    message_json = json.loads(json_data)
                    
                    # handle when client quits
                    if(message_json["identifier"]=="QUIT"):
                        message = {
                            "identifier": "Disconnection" 
                        }
                        message_json = json.dumps(message)
                        message = pack_message(MESSAGE_TYPE_JSON,message_json)
                        connection.sendall(message)
                        remove_client(connection)
                        client_thread.interrupt()
                    
                    # handle when client wants to communicate with another client
                    if(message_json["identifier"]=="Communication"):
                        print("Incoming message from: ",message_json["from"])
                        message = {
                            "identifier" : "Communication",
                            "encrypt_message" : message_json["encrypt_message"],
                            "from" : message_json["from"]
                        }
                        broadcast(message)
                        print("Message Broadcasted")
                    
                    # handle when client wants the video list
                    if(message_json["identifier"]=="Video List"):
                        message = {
                            "identifier" : "Video List",
                            "data" : list_video_files()
                        }
                        message_json = json.dumps(message)
                        message = pack_message(MESSAGE_TYPE_JSON,message_json)
                        connection.sendall(message)
                    
                    # handle when client sends the video choice it want to watch
                    if(message_json["identifier"]=="Video Choice"):
                        new_message = {
                            "identifier" : "Video Frame",
                        }
                        message_j = json.dumps(new_message)
                        message = pack_message(MESSAGE_TYPE_JSON,message_j)
                        connection.sendall(message)
                        choice = message_json["choice"]
                        choice = choice.split('_')[0]
                        client_name = message_json["from"]
                        print(f"Playing {choice} for {client_name}")
                        stream_video(connection, choice=choice)
            except ConnectionResetError:
                remove_client(client_socket=connection)
                break
            except:
                pass

    except KeyboardInterrupt:
        print("Server interrupted. Closing connections.")
        connection.close()
        sys.exit(0)  # Exit the program gracefully
    except Exception as e:
        print(f"Connection closed by client {client_address}")
    finally:
        connection.close()


if __name__ == "__main__":
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('Server starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # put socket in listening mode for TCP connections
    sock.listen(5)

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