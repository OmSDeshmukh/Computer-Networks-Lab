import socket
import cv2
import pickle
import struct

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
# video_file = "/Users/omdeshmukh/Downloads/SemVI/Computer Networks Lab/ProgrammingAssignment/Demoo.mp4"  # Replace with your video file path
videos = ["videos/240p.mp4","videos/720p.mp4","videos/1080p.mp4"]
# while True:
    # Socket Accept
client_socket, addr = server_socket.accept()
print('GOT CONNECTION FROM:', addr)

if client_socket:
    # Open the video capture object
    vid = cv2.VideoCapture(video_file)

    while vid.isOpened():
        ret, frame = vid.read()

        # Check if frame is read successfully
        if not ret:
            print("Error reading video frame.")
            break

        # Encode frame using pickle
        frame_data = pickle.dumps(frame)

        # Get the size of the frame data
        msg_size = struct.pack("Q", len(frame_data))

        # Send the frame size followed by the frame data
        client_socket.sendall(msg_size + frame_data)

        # Display frame on server (optional)
        # cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Release video capture object
    vid.release()

    # Close client socket
    client_socket.close()

# Close server socket
server_socket.close()
