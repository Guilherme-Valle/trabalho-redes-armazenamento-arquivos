import socket

server_socket = socket.socket()

port = 12345

server_socket.bind(('localhost', port))
print("socket binded to %s" %(port))

server_socket.listen(5)
print("socket is listening")

while True:
    connection, address = server_socket.accept()
    print('Got connection from', address)

    # send a thank you message to the client. encoding to send byte type.
    connection.send(f'Welcome to the server, {address[0]} ' .encode())

    recv_data = connection.recv(1024).decode('utf-8')

    print(f'File received: {recv_data}')

    # Close the connection with the client
    connection.close()

    # Breaking once connection closed
    break
