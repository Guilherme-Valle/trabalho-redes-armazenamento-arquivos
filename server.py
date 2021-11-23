import socket, shutil, json, time
from datetime import datetime
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 4444
BYTES_PER_MESSAGES = 4096
LOG_FILENAME = 'log.txt'

server_socket.bind(('localhost', PORT))
print("socket na porta %s" %(PORT))

server_socket.listen(5)
print("socket ouvindo")


def save_log(action):
    with open(LOG_FILENAME, 'a+') as file:
        action = json.loads(action)
        log = 'Operation: ' + action['method'] + ';' + \
              'Filename: ' + action['filename'] + ';' + \
              'Copies: ' + str(action['copies']) + ';' + \
              'Datetime: ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
        file.write(log)
        file.close()


def handle_client(message, addr):
    try:
       response = handle_message(message)
       save_log(message)
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
