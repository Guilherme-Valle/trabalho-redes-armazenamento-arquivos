import socket

server_socket = socket.socket()

port = 12345

server_socket.bind(('', port))
print ("socket binded to %s" %(port))

server_socket.listen(5)
print("socket is listening")

while True:
    c, addr = server_socket.accept()
    print('Got connection from', addr)

    # send a thank you message to the client. encoding to send byte type.
    c.send('Thank you for connecting'.encode())

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break
