import socket

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
    recv_data = connection.recv(1024).decode('utf-8')

    print(f'Conteúdo do arquivo recebido: {recv_data}')

    # Fecha a conexão com o cliente
    connection.close()

    # Finaliza o loop quando a conexão é fechada
    break
