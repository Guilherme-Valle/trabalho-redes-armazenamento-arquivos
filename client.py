import socket
import sys

# Cria um objeto socket
client_socket = socket.socket()

# Define a porta da conexão
port = 12345

# Conecta com a porta na conexão local
client_socket.connect(('localhost', port))

file = open('example_file.txt', 'rb')

file_data = file.read(1024)

client_socket.send(file_data)

# Receve dados do servidor e printa na tela
print(client_socket.recv(1024).decode())

# Fecha a conexão
client_socket.close()
