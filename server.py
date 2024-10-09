import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 5000))  # Porta alterada para 5000

servidor.listen()
print("Servidor ouvindo...")

cliente, end = servidor.accept()
print(f"Conexão aceita de {end}")

fim = False

while not fim:
    msg = cliente.recv(1024).decode('utf-8')

    if msg == 'tt':
        fim = True
        print("Conexão encerrada pelo cliente.")
    else:
        print(f"Cliente: {msg}")
        resposta = input("Mensagem para enviar: ")
        cliente.send(resposta.encode('utf-8'))

cliente.close()
servidor.close()



