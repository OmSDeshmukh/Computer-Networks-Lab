import socket
import cv2
import pickle
import struct
import json

video_files = {
    "240p": "videos/Video1_240p.mp4",
    "720p": "videos/Video1_720p.mp4",
    "1080p": "videos/Video1_1080p.mp4"
}

# List of videos
video_list = ["Video1_240p.mp4", "Video1_720p.mp4", "Video1_1080p.mp4"]

# Define message types
MESSAGE_TYPE_JSON = 1
MESSAGE_TYPE_FRAME = 2

def pack_message(message_type, message_data):
     # Construct the message with header
    if(message_type == MESSAGE_TYPE_FRAME):
        header = struct.pack("!BI", message_type, len(message_data))
        message = header + message_data
    elif(message_type == MESSAGE_TYPE_JSON):
        header = struct.pack("!BI", message_type, len(message_data))
        message = header + message_data.encode()
    return message


# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Host IP (replace with your server's IP)
host_ip = '0.0.0.0'
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Define the video file path
video_file = "videos/Video1_240p.mp4"  # Replace with your video file path
videos = ["videos/240p.mp4","videos/720p.mp4","videos/1080p.mp4"]
# while True:
    # Socket Accept
client_socket, addr = server_socket.accept()
print('GOT CONNECTION FROM:', addr)

video_captures = {}

for resolution, path in video_files.items():
    video_captures[resolution] = cv2.VideoCapture(path)

total_frames = min(vid.get(cv2.CAP_PROP_FRAME_COUNT) for vid in video_captures.values())
target_frames_per_resolution = int(total_frames // len(video_files))

# Define frame ranges for each resolution
frame_ranges = {
    "240p": (0, target_frames_per_resolution),
    "720p": (target_frames_per_resolution, 2*target_frames_per_resolution),
    "1080p": (2* target_frames_per_resolution, 3*target_frames_per_resolution)
}
    
if client_socket:
    # Open the video capture object
    # for resolution, frame_range in frame_ranges.items():
    #     start_frame, end_frame = frame_range

    #     vid = video_captures[resolution]
    #     vid.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    #     for _ in range(start_frame, end_frame):
    #         ret, frame = vid.read()
    #         if not ret:
    #             print("Hola")
    #             break  # Handle end of video for this resolution
            
    #         # Encode frame using pickle
    #         frame_data = pickle.dumps(frame)
    #         print(frame_data)
    #         # Get the size of the frame data
    #         msg_size = struct.pack("Q", len(frame_data))

    #         payload = msg_size + frame_data
    #         message = pack_message(MESSAGE_TYPE_FRAME, payload ) 
            
    #         # Send the frame size followed by the frame data
    #         client_socket.sendall(message)
    #         print("Frame sent")

    # # Release video capture object
    # vid.release()
    
    message = {
        "identifier" : "Testing"
    }
    message_json = json.dumps(message)
    message = pack_message(MESSAGE_TYPE_JSON,message_json)
    client_socket.sendall(message)
    # Close client socket
    client_socket.close()

# Close server socket
server_socket.close()