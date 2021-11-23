import socket, shutil, json, time
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 4444
BYTES_PER_MESSAGES = 4096

server_socket.bind(('localhost', PORT))
print("socket na porta %s" %(PORT))

server_socket.listen(5)
print("socket ouvindo")


def handle_client(message, addr):
    try:
       response = handle_message(message)
    except BrokenPipeError:
        print('[DEBUG] addr:', addr, 'Connection closed by client?')
    except Exception as ex:
        print('[DEBUG] addr:', addr, 'Exception:', ex, )
    finally:
        return

def handle_message(message):
    print(message)

while True:
    connection, address = server_socket.accept()
    print('Conectado com ', address)

    message = connection.recv(BYTES_PER_MESSAGES).decode('utf-8')

    if message:
        t = threading.Thread(target=handle_client, args=(message, address))
        t.start()
        t.join()
