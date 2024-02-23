import socket
import sys
import json
import random    

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
server_name = socket.gethostname()

print(' Server starting up on %s port %s' % server_address)
sock.bind(server_address)

# put socket in listening mode
# Listen for incoming connections
sock.listen(5)
# print('waiting for a connection')

while True:
    # connecting to the client
    connection, client_address = sock.accept()
    # print("Client connected")
    
    try:
    # Wait for a connection
        while True:
            data = connection.recv(1024)
            received_list = json.loads(data.decode())
            if received_list[1] > 100 or received_list[1] < 1:
                print(f"Integer sent {received_list[1]} by client is out of range")
                print("Closing connection with client")
                break

            print(f"Client Name: {received_list[0]}")
            print(f"Server Name: {server_name}")

            random_number = random.randint(1, 100)

            print(f"Client's random number: {received_list[1]}")
            total_sum = received_list[1] + random_number
            print(f"Sum of random numbers is {total_sum}")

            # print(f"Server's random number: {random_number}")
            print('Sending data back to the client')
            data_list = json.dumps([server_name, random_number])
            data = data_list.encode()
            connection.sendall(data)
    except Exception as e:
        print("Connection closed by client")
        break
    finally:
        connection.close()
    
print("Server Closing")
connection.close()
sock.close()



