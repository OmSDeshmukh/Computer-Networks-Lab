import socket
import sys
import json
import random    

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ("127.0.0.1", 5678)
server_name = "210010033_server"

print(' Server starting up on %s port %s' % server_address)
sock.bind(server_address)

# put socket in listening mode
# Listen for incoming connections
sock.listen(5)
print('waiting for a connection')

try:
    while True:
        connection, client_address = sock.accept()
        print(f"Client connected on {client_address}")
        received = connection.recv(1024).decode('ascii')
        filename  = received.split()[1]
        try:
            f = open(filename.split('/')[1])
        except:
            connection.send("HTTP/1.1 404 Not Found\r\n\r\n".encode('ascii'))
            output = "<html><head></head><body><h3>404 Not Found</h3></body></html>\r\n"
            connection.send(output.encode('ascii'))
            connection.close()
            continue
        output = f.read()
        connection.send("HTTP/1.1 200 OK\r\n\r\n".encode('ascii'))
        connection.sendall(output.encode('ascii'))
        connection.close()
except:
    print("Web server shutting down due to error")
    sock.close()