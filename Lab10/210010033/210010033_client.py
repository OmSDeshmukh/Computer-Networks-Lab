# We will need the following module to generate randomized lost packets 
import random 
from socket import * 
import time

# Create a UDP socket 
clientSocket = socket(AF_INET, SOCK_DGRAM) 

# Assign IP address and port number to socket
address =  ('127.0.0.1', 12000)
# clientSocket.connect(address) 
clientSocket.settimeout(1)

i = 0
while i<10:
    try:
        s = time.time()
        message = f"Ping {i} {s}"
        clientSocket.sendto(message.encode('utf_8'), address)
        message_received, address = clientSocket.recvfrom(1024) 
        e = time.time()
        print("Server Response: ",message_received.decode())
        print(f"RTT: {(e-s)} seconds")
        print("")
    except timeout:
        print("Request timed out")
        print("")
    finally:
        i+=1

clientSocket.close()