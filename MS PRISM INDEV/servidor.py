import socket
import threading

# Armazena os clientes conectados em um dicionário
clientes = {}

# Função para remover cliente da lista e fechar a conexão
def remove_cliente(cliente):
    if cliente in clientes:
        del clientes[cliente]
        cliente.close()

# Função para enviar mensagem para todos os clientes, exceto o remetente
def Adm_mensageiro_envia(mensagem, cliente_atual):
    for cliente in clientes:
        if cliente != cliente_atual:
            try:
                # Enviar o tamanho da mensagem antes dos dados
                mensagem_bytes = mensagem.encode('utf-8')
                mensagem_length = len(mensagem_bytes).to_bytes(4, byteorder='big')
                cliente.sendall(mensagem_length + mensagem_bytes)
            except:
                remove_cliente(cliente)

# Função para administrar clientes e receber mensagens
def Adm_mensageiro_recebe(cliente, endereco):
    try:
        while True:
            # Ler o tamanho da mensagem (4 bytes iniciais)
            tamanho_mensagem_bytes = b''
            while len(tamanho_mensagem_bytes) < 4:
                parte = cliente.recv(4 - len(tamanho_mensagem_bytes))
                if not parte:
                    raise ConnectionError("Conexão fechada pelo cliente")
                tamanho_mensagem_bytes += parte
            tamanho_mensagem = int.from_bytes(tamanho_mensagem_bytes, byteorder='big')

            # Ler a mensagem completa com base no tamanho
            dados_mensagem = b''
            while len(dados_mensagem) < tamanho_mensagem:
                parte = cliente.recv(tamanho_mensagem - len(dados_mensagem))
                if not parte:
                    raise ConnectionError("Conexão fechada pelo cliente")
                dados_mensagem += parte

            # Decodificar a mensagem recebida
            msg = dados_mensagem.decode('utf-8')

            if msg == 'tt':
                print(f"Cliente {endereco} desconectou.")
                remove_cliente(cliente)
                break
            else:
                # Enviar a mensagem para os outros clientes
                Adm_mensageiro_envia(msg, cliente)
    except Exception as e:
        remove_cliente(cliente)
        print(f"Erro na conexão com {endereco}: {e}")

# Função principal para iniciar o servidor
def start_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 5555))
    servidor.listen()
    print("Servidor ouvindo na porta 5555...")
    while True:
        cliente, endereco = servidor.accept()
        clientes[cliente] = endereco
        print(f"Novo cliente conectado: {endereco}")

        # Iniciar thread para o cliente conectado
        thread = threading.Thread(target=Adm_mensageiro_recebe, args=(cliente, endereco))
        thread.start()

# Inicia o servidor
start_servidor()