from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import customtkinter as ctk
import socket
import threading
from datetime import datetime

# Global variables for network and encryption
HOST = 'localhost'
PORT = 5555
cliente_socket = None
conectado = False
KEY = b'SuaChaveSecretaCom32BytesExatas!'  # Use uma chave de 32 bytes para AES-256

# Global variables for UI elements
janela = None
btn_opcao = None
messages_container = None
entrada_assunto = None
conteudo_mensagem = None
user_name = "Usuário"
# Funções de criptografia
def encrypt_message(message):
    if not message:
        print("Error: Empty message")
        return None
        
    try:
        cipher = AES.new(KEY, AES.MODE_CBC)
        iv = cipher.iv
        encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        full_message = iv + encrypted_message
        return full_message.hex()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_message(encrypted_hex):
    if not encrypted_hex:
        print("Error: Empty encrypted message")
        return None
        
    try:
        encrypted_bytes = bytes.fromhex(encrypted_hex)
        iv = encrypted_bytes[:AES.block_size]
        encrypted_message = encrypted_bytes[AES.block_size:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_message), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

# interface gráfica de usuário:
def Ui_interface_grafica():
    global janela, btn_opcao, messages_container, entrada_assunto, conteudo_mensagem

    # 1 - janela base Customtkinter.
    janela = ctk.CTk()
    janela.configure(fg_color="#0D0C10")
    janela.geometry("900x600")
    janela.title("MS Prism")
    janela.iconbitmap("Group-1.ico")
    ctk.set_appearance_mode("dark")

    # 2 - Frame Header(cabeçalho) 
    header_frame = ctk.CTkFrame(janela, height=50, fg_color="transparent")
    header_frame.pack(fill="x", side="top", pady=5)

    botao_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    botao_frame.pack(expand=True)

    # 3 - botões, sair, conectar, sobre.
    btn_opcao = ctk.CTkButton(botao_frame, text="Conectar", fg_color="White",
                                    hover_color="#505050", border_color="#505050",text_color="black",
                                    corner_radius=15, border_width=1, width=70,
                                    command=alterar_conecao)
    btn_opcao.pack(side="left", padx=30, pady=10)

    btn_sobre = ctk.CTkButton(botao_frame, text="Sobre", fg_color="White",
                             hover_color="#505050", border_color="#505050",text_color="black",
                             corner_radius=15, border_width=1, width=70,
                             command=pagina_sobre)
    btn_sobre.pack(side="left", padx=30, pady=10)
    
    btn_sair = ctk.CTkButton(botao_frame, text="Sair", fg_color="White", hover_color="red", 
                                border_color="#505050", text_color="black",
                                border_width=1, corner_radius=16, width=70,
                                command=funcao_sair)
    btn_sair.pack(side="left", padx=30, pady=10)

    # 4 - Frame Esquerdo(Mensagens Recebidas.)
    frame_esquerdo = ctk.CTkFrame(janela, fg_color="#0D0C10",
                              border_color="#505050", border_width=1, corner_radius=10)
    frame_esquerdo.pack(side="left", fill="both", expand=True, padx=10, pady=(5, 20))

    titulo_recebidas = ctk.CTkLabel(frame_esquerdo, text="Mensagens recebidas:", 
                                   text_color="gray", font=ctk.CTkFont("Times", 22))
    titulo_recebidas.pack(padx=10, pady=10)

    messages_container = ctk.CTkScrollableFrame(frame_esquerdo, fg_color="#0D0C10")
    messages_container.pack(fill="both", expand=True, padx=5, pady=5)

    # 5 - Frame Direito(Ler e enviar mensagens.)
    frame_direito = ctk.CTkFrame(janela, width=500, fg_color="#0D0C10",
                                corner_radius=10, border_width=1, border_color="#505050")
    frame_direito.pack(side="right", fill="both", expand=True, padx=10, pady=(5, 20))

    titulo_painel = ctk.CTkLabel(frame_direito, text="Painel",
                                font=ctk.CTkFont("Times", 40))
    titulo_painel.pack(anchor="w", padx=10, pady=10)

    titulo_painel = ctk.CTkLabel(frame_direito, text="Digite o assunto:", text_color="#242328", 
                                font=ctk.CTkFont("Times", 15))
    titulo_painel.pack(anchor="w", padx=10, pady=10)

    # 6 - Entrada de dados de mensagens.
    entrada_assunto = ctk.CTkEntry(frame_direito, placeholder_text="Assunto:",
                                  width=500, height=40, border_width=1,
                                  corner_radius=10, fg_color="#242328",
                                  font=ctk.CTkFont(size=15))
    entrada_assunto.pack(anchor="w", padx=10, pady=5)

    titulo_painel = ctk.CTkLabel(frame_direito, text="Digite sua mensagem:", text_color="#242328", 
                                font=ctk.CTkFont("Times", 15))
    titulo_painel.pack(anchor="w", padx=10, pady=10)

    mensagem_frame = ctk.CTkFrame(frame_direito, fg_color="#242328",
                                 corner_radius=10, border_width=1,
                                 border_color="#505050")
    mensagem_frame.pack(fill="both", expand=True, padx=10, pady=10)

    conteudo_mensagem = ctk.CTkTextbox(mensagem_frame, wrap="word",
                                      width=300, height=200, fg_color="#242328",
                                      text_color="white", font=ctk.CTkFont(size=15,))
    conteudo_mensagem.pack(fill="both", expand=True, padx=10, pady=10)
    conteudo_mensagem.insert("0.0", "Msg: ")

    # 7 - botão enviar.
    btn_enviar = ctk.CTkButton(frame_direito, text="Enviar", fg_color="white",text_color="black",
                              hover_color="#333333", corner_radius=16,   command=enviar_mensagem)
    btn_enviar.pack(anchor="e", padx=10, pady=10)

def conectar_servidor():
    global cliente_socket, conectado, btn_opcao
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((HOST, PORT))
        conectado = True
        btn_opcao.configure(text="Desconectar")
        
        # Thread que permite o recebimento de mensagens.
        ouvir_mensagens_thread = threading.Thread(target=recebendo_mensagens)
        ouvir_mensagens_thread.daemon = True
        ouvir_mensagens_thread.start()
    except Exception as e:
        Alerta_ERRO("Erro", f"Não foi possível conectar: {str(e)}")

def funcao_sair():
    if conectado:
        desconectar()
    janela.quit()

def desconectar():
    global cliente_socket, conectado, btn_opcao
    if cliente_socket:
        try:
            cliente_socket.close()
        except:
            pass
        cliente_socket = None
        conectado = False
        btn_opcao.configure(text="Conectar")

def alterar_conecao():
    if not conectado:
        conectar_servidor()
    else:
        desconectar()

def pagina_sobre():
    alerta = ctk.CTkToplevel()
    alerta.title("Sobre")
    alerta.geometry("600x450")
    alerta.iconbitmap("Group-1.ico")
    alerta.configure(fg_color="#275EDF")

    caixa_de_texto = ctk.CTkLabel(alerta,text="Sobre",text_color="white",
                                font=ctk.CTkFont("Arial", 40))
    caixa_de_texto.pack(pady=20,)

    caixa_de_texto = ctk.CTkLabel(
    alerta,
    text=(
        "   O Prism é um aplicativo de envio e recebimento de mensagens\n"
        "desenvolvido para proporcionar uma comunicação rápida,\n"
        "segura e confiável entre usuários. Projetado para ser intuitivo,\n"
        "o Prism oferece uma interface simples, com recursos que permitem\n"
        "a leitura e o gerenciamento de mensagens diretamente na plataforma.\n"
        "Inclui a possibilidade de ler, ignorar ou responder rapidamente\n"
        "as comunicações recebidas.\n\n"
        
        "   Licenciamento de Software:\n"
        "   O Prism é distribuído como software livre e de código aberto,\n"
        "sob a licença MIT, permitindo que qualquer pessoa use, modifique\n"
        "e distribua o código-fonte para quaisquer fins, seja pessoal ou\n"
        "comercial. Essa licença garante que o Prism pode ser aprimorado\n"
        "pela comunidade e adaptado para diversas necessidades, enquanto\n"
        "mantém seu compromisso com a acessibilidade e a segurança."
    ),
    text_color="white",
    font=ctk.CTkFont("Arial", 16)
)
    caixa_de_texto.pack(pady=20)

def enviar_mensagem():
    if not conectado:
        Alerta_ERRO("Erro", "Não está conectado ao servidor")
        return

    assunto = entrada_assunto.get()
    mensagem = conteudo_mensagem.get("1.0", "end-1c")

    if not assunto or not mensagem:
        Alerta_ERRO("Erro", "Preencha todos os campos")
        return

    try:
        encrypted_message = encrypt_message(mensagem)
        if encrypted_message is None:
            Alerta_ERRO("Erro", "Erro ao criptografar a mensagem")
            return

        mensagem_formatada = f"{assunto}|||{encrypted_message}|||{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        mensagem_bytes = mensagem_formatada.encode('utf-8')
        mensagem_length = len(mensagem_bytes).to_bytes(4, byteorder='big')
        cliente_socket.sendall(mensagem_length + mensagem_bytes)

        entrada_assunto.delete(0, 'end')
        conteudo_mensagem.delete("1.0", "end")
        conteudo_mensagem.insert("0.0", "Msg: ")

    except Exception as e:
        Alerta_ERRO("Erro", f"Erro ao enviar: {str(e)}")

def recebendo_mensagens():
    buffer = b''
    while conectado:
        try:
            # Ler o tamanho da mensagem
            while len(buffer) < 4:
                data = cliente_socket.recv(4 - len(buffer))
                if not data:
                    raise ConnectionResetError()
                buffer += data
            mensagem_length = int.from_bytes(buffer[:4], byteorder='big')
            buffer = buffer[4:]

            # Ler a mensagem completa
            while len(buffer) < mensagem_length:
                data = cliente_socket.recv(mensagem_length - len(buffer))
                if not data:
                    raise ConnectionResetError()
                buffer += data

            mensagem_completa = buffer[:mensagem_length]
            buffer = buffer[mensagem_length:]

            data_str = mensagem_completa.decode('utf-8')
            parts = data_str.split("|||")
            if len(parts) == 3:
                assunto, encrypted_message, timestamp = parts
                mensagem = decrypt_message(encrypted_message)
                if mensagem is not None:
                    preview_mensagem(assunto, mensagem)
                else:
                    print("Erro ao descriptografar a mensagem")
            else:
                print("Formato de mensagem inválido")

        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

    desconectar()

def preview_mensagem(assunto, mensagem):
    frame_mensagem = ctk.CTkFrame(messages_container, fg_color="#242328",
                                   corner_radius=10,border_color="#505050",
                                    border_width=1,)
    frame_mensagem.pack(fill="x", padx=10, pady=5)

    label_assunto = ctk.CTkLabel(frame_mensagem, text=assunto, font=ctk.CTkFont("Arial", 16))
    label_assunto.pack(anchor="w", padx=10, pady=5)

    texto_preview = ctk.CTkLabel(frame_mensagem, text=mensagem[:50] + "..." if len(mensagem) > 50 else mensagem,
                                font=ctk.CTkFont(size=10), wraplength=180)
    texto_preview.pack(anchor="w", padx=10, pady=5)

    def ler_mensagem():
        conteudo_mensagem.delete("1.0", "end")
        conteudo_mensagem.insert("0.0", mensagem)
        entrada_assunto.delete(0, 'end')
        entrada_assunto.insert(0, assunto)

    btn_ler = ctk.CTkButton(frame_mensagem, text="Ler", fg_color="white",
                           text_color="black", width=70, command=ler_mensagem)
    btn_ler.pack(side="left", padx=10, pady=5)

    btn_ignorar = ctk.CTkButton(frame_mensagem, text="Ignorar", fg_color="gray",
                               text_color="white", width=70,border_width=1, border_color="#505050",
                               command=lambda: frame_mensagem.destroy())
    btn_ignorar.pack(side="left", padx=5, pady=5)

def Alerta_ERRO(title, message):
    alerta = ctk.CTkToplevel()
    alerta.title("ERRO")
    alerta.geometry("300x150")
    alerta.iconbitmap("Group-1.ico")
    alerta.configure(fg_color="#275EDF")

    Erro_mensagem = ctk.CTkLabel(master=alerta, text=f'Erro: {title} {message}')
    Erro_mensagem.pack(pady=20)

    btn_fechar = ctk.CTkButton(alerta, text="Ok", command=alerta.destroy, text_color="black",
                              fg_color="White", hover_color="red")
    btn_fechar.pack(pady=10)

if __name__ == "__main__":
    Ui_interface_grafica()
    janela.mainloop()