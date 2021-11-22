import socket
import sys
import time
# Cria um objeto socket
client_socket = socket.socket()

# Define a porta da conexão
port = 12345

# Conecta com a porta na conexão local
client_socket.connect(('localhost', port))

# Nome do arquivo
file_name = 'example_file.txt'

# Arquivo
file = open(file_name, 'rb')
file_data = file.read(1024)

# Numero de copias
copies = '2'

client_socket.send(file_name.encode())

time.sleep(1)

client_socket.send(file_data)

time.sleep(1)

client_socket.send(copies.encode())

# Receve dados do servidor e printa na tela
print(client_socket.recv(1024).decode())

# Fecha a conexão
client_socket.close()
