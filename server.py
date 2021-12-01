import socket, shutil, json, time, os
from datetime import datetime
import threading
from pathlib import Path

PORT = 1234
BYTES_PER_MESSAGES = 4096
LOG_FILENAME = 'log.txt'

def adicionar_arquivo_servidores(antigo_registro_gerenciamento, file_info):
    if antigo_registro_gerenciamento is None:
        for number in range(int(file_info["copies"])):
            nome_servidor = "servidores/armazenamento_servidor_" + str(number)
            replicar_arquivo(nome_servidor, file_info["filename"], file_info["content"])

    else:
        if int(antigo_registro_gerenciamento["copies"]) > int(file_info["copies"]):
            servidores_para_excluir = range(int(file_info["copies"]), int(antigo_registro_gerenciamento["copies"]))

            for numero_servidor in servidores_para_excluir:
                nome_servidor = "servidores/armazenamento_servidor_" + str(numero_servidor)
                caminho_arquivo = os.path.join(nome_servidor, file_info["filename"])
                os.remove(caminho_arquivo)
        else:
            servidores_para_adicionar = range(int(antigo_registro_gerenciamento["copies"]), int(file_info["copies"]))
            caminho_arquivo_1 = os.path.join("servidores/armazenamento_servidor_" + str(0), file_info["filename"])
            for numero_servidor in servidores_para_adicionar:
                nome_servidor = "servidores/armazenamento_servidor_" + str(numero_servidor)
                servidor_existe = os.path.isdir(nome_servidor)
                if not servidor_existe:
                    os.mkdir(nome_servidor)
                shutil.copy2(caminho_arquivo_1, nome_servidor)
                
def receber_arquivo(file_info):
    # Recebe arquivo do cliente

    print('\n\n\nNome do arquivo: {filename}\nCopias: {copies}\nConteúdo: {content}'.format(**file_info))
    # print(file_info['content'].decode())

    arquivo_gerenciamento = open('arquivo_gerenciamento.json', 'r')
    conteudo_arquivo_gerenciamento = json.loads(arquivo_gerenciamento.read())
    arquivo_gerenciamento.close()

    
    arquivo_gerenciamento_escrita = open('arquivo_gerenciamento.json', 'w')
    novo_registro_gerenciamento = {
        "filename": file_info["filename"],
        "copies": file_info["copies"]
    }

    try:
        conteudo_arquivo_gerenciamento.append(novo_registro_gerenciamento)
        adicionar_arquivo_servidores(None, file_info)
        arquivo_gerenciamento_escrita.write(json.dumps(conteudo_arquivo_gerenciamento))
        arquivo_gerenciamento_escrita.close()
    except:
        arquivo_gerenciamento_escrita.close()

def editar_replicas(file_info):
    arquivo_gerenciamento = open('arquivo_gerenciamento.json', 'r')
    conteudo_arquivo_gerenciamento = json.loads(arquivo_gerenciamento.read())
    arquivo_gerenciamento.close()

    indice_existente = next(iter([i for i, item in enumerate(conteudo_arquivo_gerenciamento) if item["filename"] == file_info["filename"]]), None)
    antigo_registro_gerenciamento = conteudo_arquivo_gerenciamento[indice_existente]
    adicionar_arquivo_servidores(antigo_registro_gerenciamento, file_info)
    
    try:
        novo_registro_gerenciamento = {
            "filename": file_info["filename"],
            "copies": file_info["copies"]
        }
        conteudo_arquivo_gerenciamento[indice_existente] = novo_registro_gerenciamento
        arquivo_gerenciamento_escrita = open('arquivo_gerenciamento.json', 'w')
        arquivo_gerenciamento_escrita.write(json.dumps(conteudo_arquivo_gerenciamento))
        arquivo_gerenciamento_escrita.close()
    except:
        arquivo_gerenciamento_escrita.close()

def replicar_arquivo(nome_servidor, nome_arquivo, conteudo_arquivo):
    servidor_existe = os.path.isdir(nome_servidor)
    if not servidor_existe:
        os.mkdir(nome_servidor)

    caminho_arquivo = os.path.join(nome_servidor, nome_arquivo)
    escrevendo_arquivo = open(caminho_arquivo, 'wb')

    escrevendo_arquivo.write(conteudo_arquivo.encode('utf-8'))
    escrevendo_arquivo.close()
    
def save_log(action):
    if 'copies' in action:
        copies = str(action['copies'])
    else:
        copies = ''

    with open(LOG_FILENAME, 'a+') as file:
        log = 'Operation: ' + action['method'] + ';' + \
              'Filename: ' + action['filename'] + ';' + \
              'Copies: ' + copies + ';' + \
              'Datetime: ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
        file.write(log)
        file.close()

def enviar_arquivo(message):
    filename = message['filename']
    for path, subdirs, files in os.walk(str(Path().absolute()) +'/servidores'):
        try:
            print(path+'/'+filename)
            file = open(path+'/'+filename, 'r')

            content = file.read()
            return {'filename': filename, 'content': content}
        except Exception as e:
            print("Não encontrado em: " + path)
            continue
    return {'filename': filename, 'content': None, 'error': 'Not Found'}


def enviar_log():
    logs = []
    with open(LOG_FILENAME) as file:
        while line := file.readline().rstrip():
            logs.append(line)

    return logs


def handle_client(connection, message, addr):
    try:
       message = json.loads(message)
       response = handle_message(message)

       if message['method'] != 'logs':
           save_log(message)

       if response:
           connection.send(json.dumps(response).encode('utf-8'))

    except BrokenPipeError:
        print('[DEBUG] addr:', addr, 'Connection closed by client?')
    except Exception as ex:
        print('[DEBUG] addr:', addr, 'Exception:', ex, )
    finally:
        return


def handle_message(message):
    print(message)
    if message["method"] == 'upload':
        receber_arquivo(message)
        return None
    if message["method"] == 'edit':
        editar_replicas(message)
        return None
    if message["method"] == 'request':
        return enviar_arquivo(message)
    if message["method"] == 'logs':
        return enviar_log()


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('localhost', PORT))
    print("socket na porta %s" %(PORT))

    server_socket.listen(5)
    print("socket ouvindo")

    # enviar_arquivo({'filename': 'arq1.txt'})

    while True:
        connection, address = server_socket.accept()
        print('Conectado com ', address)

        message = connection.recv(BYTES_PER_MESSAGES).decode('utf-8')

        if message:
            t = threading.Thread(target=handle_client, args=(connection, message, address))
            t.start()
            t.join()