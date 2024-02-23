import socket
import random
import json

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_info = ("localhost",12345)

client_socket.connect(server_info)

try:
    while True:
        data = [1,2]
        data_json = json.dumps(data)
        client_socket.sendall(data_json.encode())
        
        data_received = client_socket.recv(1024)
        data_received_json = data_received.decode()
        data_r_list = json.loads(data_received_json)
        
        #do what is wanted with data
        break #to stop the loop
except:
    print("Some error occured")
finally:
    client_socket.close()