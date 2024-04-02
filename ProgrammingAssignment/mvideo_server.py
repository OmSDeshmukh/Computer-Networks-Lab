# import socket
# import cv2
# import pickle
# import struct

# # Video file definitions (replace with your paths)
# video_files = {
#     "240p": "videos/240p.mp4",
#     "720p": "videos/720p.mp4",
#     "1080p": "videos/1080p.mp4"
# }

# # Socket creation
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # Host IP (replace with your server's IP)
# host_ip = '0.0.0.0'
# print('HOST IP:', host_ip)
# port = 10001
# socket_address = (host_ip, port)

# # Socket bind
# server_socket.bind(socket_address)

# # Socket listen
# server_socket.listen(5)
# print("LISTENING AT:", socket_address)

# while True:
#     # Client connection and video request handling
#     client_socket, addr = server_socket.accept()
#     print('GOT CONNECTION FROM:', addr)

#     if client_socket:
#         # Create video capture objects for each resolution
#         video_captures = {}
#         for resolution, path in video_files.items():
#             video_captures[resolution] = cv2.VideoCapture(path)
#         print("Videos captured!")

#         # Video streaming loop
#         total_frames = min(vid.get(cv2.CAP_PROP_FRAME_COUNT) for vid in video_captures.values())
#         target_frames_per_resolution = total_frames // len(video_files)

#         for resolution in video_files:
#             frame_count = 0
#             capture = video_captures[resolution]
#             while frame_count < target_frames_per_resolution:
#                 ret, frame = capture.read()
#                 if not ret:
#                     break  # Handle end of video for this resolution

#                 frame_data = pickle.dumps(frame)
#                 msg_size = struct.pack("Q", len(frame_data))
#                 client_socket.sendall(msg_size + frame_data)

#                 frame_count += 1

#         # Cleanup
#         for capture in video_captures.values():
#             capture.release()

#         client_socket.close()

# # Close server socket
# server_socket.close()

import socket
import cv2
import pickle
import struct

# Video file definitions (replace with your paths)
video_files = {
    "240p": "videos/240p.mp4",
    "720p": "videos/720p.mp4",
    "1080p": "videos/1080p.mp4"
}

# Socket creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Host IP (replace with your server's IP)
host_ip = '0.0.0.0'
print('HOST IP:', host_ip)
port = 10001
socket_address = (host_ip, port)

# Socket bind
server_socket.bind(socket_address)

# Socket listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

while True:
    # Client connection and video request handling
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)

    if client_socket:
        # Create video capture objects for each resolution
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

        # Video streaming loop
        for resolution, frame_range in frame_ranges.items():
            start_frame, end_frame = frame_range

            vid = video_captures[resolution]
            vid.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            for _ in range(start_frame, end_frame):
                ret, frame = vid.read()
                if not ret:
                    break  # Handle end of video for this resolution

                frame_data = pickle.dumps(frame)
                msg_size = struct.pack("Q", len(frame_data))
                client_socket.sendall(msg_size + frame_data)

        # Cleanup
        for capture in video_captures.values():
            capture.release()

        client_socket.close()

# Close server socket
server_socket.close()
