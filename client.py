import socket
import sys
import time
import json
import os
from simple_term_menu import TerminalMenu

PORT = 4444
BYTES_PER_MESSAGES = 4096

def close(sock):
     sock.close()

def read_file():
    filename = None
    file_content = None

    while filename == None:
        try:
            filename = str(input('Digite o nome do arquivo: '))

            if filename in ['\n', '']:
                print('aborting')
                sys.exit(0)

            file = open(filename, 'rb')
            return filename, str(file.read(1024))
        except:
            print('Houve um erro ao tentar ler o arquivo. Tente novamente.')

def open_socket_connection():
    client_socket = socket.socket()
    tryAgain = 's'

    while tryAgain in ['s', 'S', '']:
        try:
            client_socket.connect(('localhost', PORT))

            return client_socket
        except ConnectionRefusedError:
            print('Não foi possivel iniciar conexão. Verifique se o servidor está rodando na porta {port}'.format(port=PORT))
            tryAgain = str(input('Tentar novamente? (S/n) '))
            
    sys.exit()

def upload():
    conection = open_socket_connection()
    filename, content = read_file()
    copies = int(input('Numero de cópias: '))

    message = json.dumps({
        'method': 'upload',
        'filename': filename,
        'content': content,
        'copies': copies
    },  ensure_ascii=False).encode('utf8')

    conection.send(message)

def edit():
    conection = open_socket_connection()
    filename = str(input('Nome do arquivo: '))
    copies = int(input('Numero de cópias: '))
    message = json.dumps({
        'method': 'edit',
        'filename': filename,
        'copies': copies
    },  ensure_ascii=False).encode('utf8')

    conection.send(message)

def do_exit():
     sys.exit(0)

def menu():
    options = [
        {'title': "Enviar novo arquivo", "action" :upload},
        {'title': "Atualizar Numero de cópias", "action" :edit},
        {'title': "Sair", "action": do_exit}
    ]
    terminal_menu = TerminalMenu([option['title'] for option in options])
    selected_index = terminal_menu.show()
    selected = options[selected_index]
    selected['action']()


if __name__ == '__main__':
    while True:
        menu()
        os.system('cls' if os.name == 'nt' else 'clear')