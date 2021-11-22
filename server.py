import socket
import shutil

server_socket = socket.socket()

port = 12345

server_socket.bind(('localhost', port))
print("socket na porta %s" %(port))

server_socket.listen(5)
print("socket ouvindo")

while True:
    connection, address = server_socket.accept()
    print('Conectado com ', address)

    # Envia mensagem para o cliente
    connection.send(f'Bem-vindo ao servidor, {address[0]} ' .encode())

    # Recebe arquivo do cliente
    file_name = connection.recv(1024).decode('utf-8')
    print(f'Nome do arquivo: {file_name}')

    file_content = connection.recv(1024).decode('utf-8')
    print(f'Conteúdo do arquivo recebido: {file_content}')

    file_copies = connection.recv(1024).decode('utf-8')
    print(f'Número de cópias: {file_copies}')



    # Fecha a conexão com o cliente
    connection.close()

    # Finaliza o loop quando a conexão é fechada
    break
