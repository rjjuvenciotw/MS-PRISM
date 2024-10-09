import socket 

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(('localhost', 5000))  # Porta alterada para 5000

fim = False

print("Digite 'tt' para terminar o chat")

while not fim:
    mensagem = input("Mensagem: ")

    cliente.send(mensagem.encode("utf-8"))

    if mensagem == 'tt':
        fim = True
    else:
        msg = cliente.recv(1024).decode('utf-8')
        print(f"Servidor: {msg}")

cliente.close()



