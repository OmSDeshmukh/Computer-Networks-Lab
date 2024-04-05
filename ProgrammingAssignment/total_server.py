# server handling everything
import socket
import sys
import json
import threading
import cv2

video_files = [["videos/Video1_240p.mp4", "videos/Video1_720p.mp4", "videos/Video1_1080p.mp4"],
               ["videos/Video2_240p.mp4", "videos/Video2_720p.mp4", "videos/Video2_1080p.mp4"],
               ["videos/Video3_240p.mp4", "videos/Video3_720p.mp4", "videos/Video3_1080p.mp4"]]

# List of videos
video_list = [["Video1_240p.mp4", "Video1_720p.mp4", "Video1_1080p.mp4"],
              ["Video2_240p.mp4", "Video2_720p.mp4", "Video2_1080p.mp4"],
              ["Video3_240p.mp4", "Video3_720p.mp4", "Video3_1080p.mp4"]]

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
def broadcast_dictionary(*args):
    global client_details, client_socks
    # with lock: # gimini
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

def stream_video(connection, choice):
    videos = video_files[choice-1]
    frame_counts = [0] * len(videos)
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
            connection.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)
            
            # print("Frame sent")
            # Switch to the next file if one-third of frames sent
            if  current_frame >= end_frame:
                current_file_index += 1
                break
        
        cap.release()
    print("Finished")

    # to aknowledge that streaming has finished
    connection.sendall('0'.encode().ljust(16))

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
            broadcast_dictionary(temp)
                    

def handle_client_connection(connection, client_address):
    global client_details, client_socks
    try:
        # welcome_string1 = "Enter your name: "
        name_received = connection.recv(1024).decode()
        print("Name received:", name_received)
        
        # welcome_string2 = "Enter the public key: "
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
            
            if(message_json["identifier"]=="Video List"):
                message = {
                    "identifier" : "Video List",
                    "data" : video_list
                }
                connection.sendall(json.dumps(message).encode())
            
            if(message_json["identifier"]=="Video Choice"):
                message = {
                    "identifier" : "Video Frame",
                }
                connection.sendall(json.dumps(message).encode())
                
                choice = message_json["choice"]
                choice_no = int(choice[5])
                # choice_quality = choice.substr(7)
                client_name = message_json["from"]
                print(f"Playing {choice} for {client_name}")
                stream_video(connection, choice=choice_no)
            

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