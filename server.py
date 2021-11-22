import socket, shutil, json

server_socket = socket.socket()

PORT = 12345
BYTES_PER_MESSAGES = 4096

server_socket.bind(('localhost', PORT))
print("socket na porta %s" %(PORT))

server_socket.listen(5)
print("socket ouvindo")

while True:
    connection, address = server_socket.accept()
    print('Conectado com ', address)

    # Envia mensagem para o cliente
    connection.send(f'Bem-vindo ao servidor, {address[0]} ' .encode())

    # Recebe arquivo do cliente
    file = connection.recv(BYTES_PER_MESSAGES).decode('utf-8')
    file_info = json.loads(file)

    print('\n\n\nNome do arquivo: {filename}\nCopias: {copies}\nConteúdo: {content}'.format(**file_info))



    # Fecha a conexão com o cliente
    connection.close()

    # Finaliza o loop quando a conexão é fechada
    break
