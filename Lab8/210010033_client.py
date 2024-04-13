import socket
import ssl
from base64 import b64encode 

userEmail = "smtplab23@gmail.com" 
userPassword = "lmvgusmmhxkmzoti" 
userDestinationEmail = input("Enter Email Destination: ") 
userSubject = input("Enter Subject: ") 
userBody = input("Enter Message: ") 
msg = '{}.\r\n I love computer networks!'.format(userBody) 

# Choose a mail server (e.g. Google mail server) and call it mailserver 
# #Fill in start 
mailserver = ("smtp.gmail.com",587)
# #Fill in end 

# Create socket called clientSocket and establish a TCP connection with mailserver 
#Fill in start 
client_name = "210010033_mail_client"

# Create a TCP/IP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = mailserver
print(f"connecting to {server_address[0]} port {server_address[1]}")
try:
    clientSocket.connect(server_address)
except:
    print("Cannot connect to the server")

#Fill in end 

recv = clientSocket.recv(1024).decode() 
print(recv) 

if recv[:3] != '220': 
    print('220 reply not received from server.') 
    
# Send HELO command and print server response. 
heloCommand = 'HELO Alice\r\n' 
clientSocket.send(heloCommand.encode()) 
recv1 = clientSocket.recv(1024).decode() 
print(recv1) 

if recv1[:3] != '250': 
    print('250 reply not received from server.') 
    
    
#account authentication 
clientSocket.send("STARTTLS\r\n".encode()) 
clientSocket.recv(1024) 
sslClientSocket = ssl.wrap_socket(clientSocket) 
sslClientSocket.send("AUTH LOGIN\r\n".encode()) 
print(sslClientSocket.recv(1024)) 
sslClientSocket.send(b64encode(userEmail.encode()) + "\r\n".encode())
print(sslClientSocket.recv(1024))
sslClientSocket.send(b64encode(userPassword.encode()) + "\r\n".encode()) 
print(sslClientSocket.recv(1024)) 

# Send MAIL FROM command and print server response.
#Fill in start 
sslClientSocket.sendall(f"MAIL FROM:<{userEmail}>\r\n".encode()) 
res = sslClientSocket.recv(1024).decode() 
print(res)
#Fill in end 

# Send RCPT TO command and print server response.
# Fill in start
sslClientSocket.send(f"RCPT TO:<{userDestinationEmail}>\r\n".encode()) 
res = sslClientSocket.recv(1024).decode() 
print(res)
# Fill in end 

# Send DATA command and print server response. 
#Fill in start 
sslClientSocket.send("DATA\r\n".encode()) 
res = sslClientSocket.recv(1024).decode() 
print(res)
#Fill in end 

# Send message data. 
#Fill in start 
sslClientSocket.send(f"SUBJECT: {userSubject}\r\n".encode()) 
sslClientSocket.send(msg.encode()) 
#Fill in end 


# Message ends with a single period. 
#Fill in start 
sslClientSocket.send("\r\n.\r\n".encode())
res = sslClientSocket.recv(1024).decode() 
print(res)
#Fill in end 


# Send QUIT command and get server response. 
#Fill in start 
sslClientSocket.send("QUIT\r\n".encode())
print("done")
#Fill in end