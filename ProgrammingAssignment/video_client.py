import socket
import cv2
import pickle
import struct

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '0.0.0.0'  # Replace with server IP
port = 10001
client_socket.connect((host_ip, port))
flag=0
data = b""
payload_size = struct.calcsize("Q") # an interger of type long long (128 bits maybe)
# payload refers to the max size we can have for the incoming messag
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(16 * 1024)  # 4K
        if not packet:
            flag=1
            break
        data += packet
    if flag:
        break
    packed_msg_size = data[:payload_size] # to get the size of the video which is encoded by the server while sending the video
    data = data[payload_size:] # actual video data
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size: # if we still haven't revceived the entire file
        data += client_socket.recv(16 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    # Display received frame
    frame = cv2.resize(frame, (1080,720))
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Close client socket
client_socket.close()
