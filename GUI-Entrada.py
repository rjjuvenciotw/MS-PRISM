import customtkinter as ctk

from PIL import Image
from customtkinter import CTkImage

credenciais_validas = ['A23B', 'L22H', 'WV35' , "A01"]

janela = ctk.CTk() 

janela.configure(fg_color="#0D0C10")
janela.geometry("900x600")
janela.title("Prism")
ctk.set_appearance_mode("dark")
janela.iconbitmap("Group-1.ico")

titulo = ctk.CTkLabel(
    janela, 
    text="PRISM",
    font=("Times New Roman", 174),
    text_color="white",
    height=300    
)
titulo.pack(padx=10, pady=10)

subtitulo = ctk.CTkLabel(
    master=janela,
    text_color="gray", 
    text="Digite sua credencial e nome de usuário para entrar no programa:",
    font=("Helvetica", 16, "bold")
)
subtitulo.pack(padx=10, pady=10)

# Caixa de entrada de dados;

User_nome = ctk.CTkEntry(
    janela, 
    placeholder_text="Digitar seu nome de usuário:",
    width=320,
    height=36,
    corner_radius=13,
    border_width=1,
    border_color="#505050",
    show="*",
)
User_nome.pack(padx=10, pady=10) 

credencialEntrada = ctk.CTkEntry(
    janela, 
    placeholder_text="Digitar credencial:",
    width=320,
    height=36,
    corner_radius=13,
    border_width=1,
    border_color="#505050",
    show="*",
)
credencialEntrada.pack(padx=10, pady=10) 

# botão para entrar no programa; _input faz diferença '-'
def click_botao():

    credencialEntrada_input = credencialEntrada.get()
    if credencialEntrada_input in credenciais_validas:
        print("Credencial valida!!")

    else:
        print("crednecial invalida, tente novamente '-'")

# Botão para entrar no programa
botao_entrar = ctk.CTkButton(
    janela, 
    text="Entrar", 
    command=click_botao, 
    fg_color="transparent", 
    border_width=1, 
    border_color="white", 
    hover_color="gray" ,
)
botao_entrar.pack(padx=10, pady=10) 

janela.mainloop()

