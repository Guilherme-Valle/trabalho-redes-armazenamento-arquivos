import socket
import sys

# Create a socket object
client_socket = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
client_socket.connect(('localhost', port))

file = open('example_file.txt', 'rb')

file_data = file.read(1024)

client_socket.send(file_data)

# receive data from the server and decoding to get the string.
print(client_socket.recv(1024).decode())

# close the connection
client_socket.close()
