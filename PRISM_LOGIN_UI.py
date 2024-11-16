import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

# Configurações globais
credenciais_validas = ['A23B', 'L22H', 'WV35', 'A01']

# Configuração da janela principal
janela = ctk.CTk()
janela.configure(fg_color="#1E1E1E")
janela.geometry("900x600")
janela.title("Prism")
janela.resizable(False, False)
ctk.set_appearance_mode("dark")
janela.iconbitmap("MIDIA/Group-1.ico")

# Background
background_image = CTkImage(Image.open("MIDIA/mg2.png"), size=(900, 600))
background_label = ctk.CTkLabel(janela, image=background_image, text="")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Frame principal com tamanho aumentado e borda interna maior
frame_centro = ctk.CTkFrame(
    janela,
    fg_color="black",
    corner_radius=20,
    width=520,         # Aumenta a largura para 520 pixels
    height=720,        # Aumenta a altura para 720 pixels
    border_width=10,   # Define a espessura da borda interna
    border_color="white"  # Define a cor da borda
)
frame_centro.place(relx=0.5, rely=0.5, anchor='center')

# Frame interno para padding e conteúdo
inner_frame = ctk.CTkFrame(
    frame_centro,
    fg_color="black",
    corner_radius=10
)
inner_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Widgets dentro do inner_frame
msprism = ctk.CTkLabel(
    inner_frame,
    fg_color="transparent",
    text="MSPRISM",
    font=("Times", 50, "bold"),
    text_color="white",
)
msprism.pack(pady=(30, 10))

# Título
titulo = ctk.CTkLabel(
    inner_frame,
    text="Entrar",
    font=("Helvetica", 30, "bold"),
    text_color="white",
)
titulo.pack(pady=(10, 5))

# Subtítulo
subtitulo = ctk.CTkLabel(
    inner_frame,
    text="Digite suas credenciais para acessar",
    text_color="#BBBBBB",
    font=("Helvetica", 14)
)
subtitulo.pack(pady=(0, 20))

# Frame do campo de usuário
user_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
user_frame.pack(fill="x", padx=40, pady=(0, 15))

user_icon_label = ctk.CTkLabel(
    user_frame,
    text="👤",
    font=("Helvetica", 16),
    text_color="#BBBBBB"
)
user_icon_label.pack(side="left", padx=(0, 10))

user_nome = ctk.CTkEntry(
    user_frame,
    placeholder_text="Nome de usuário",
    height=40,
    corner_radius=8,
    border_width=2,
    border_color="#505050",
    font=("Helvetica", 14)
)
user_nome.pack(side="left", fill="x", expand=True)

# Frame do campo de credencial
credencial_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
credencial_frame.pack(fill="x", padx=40, pady=(0, 20))

key_icon_label = ctk.CTkLabel(
    credencial_frame,
    text="🔑",
    font=("Helvetica", 16),
    text_color="#BBBBBB"
)
key_icon_label.pack(side="left", padx=(0, 10))

credencial_entrada = ctk.CTkEntry(
    credencial_frame,
    placeholder_text="Credencial",
    height=40,
    corner_radius=8,
    border_width=2,
    border_color="#505050",
    font=("Helvetica", 14),
    show="•"
)
credencial_entrada.pack(side="left", fill="x", expand=True)

# Label para mensagens de status
status_label = ctk.CTkLabel(
    inner_frame,
    text="",
    text_color="#FF5555",
    font=("Helvetica", 12)
)
status_label.pack(pady=(0, 10))

def iniciar_programa():
    janela.destroy()
    # Aqui você pode abrir a próxima janela ou iniciar o programa principal

def verificar_credenciais():
    username = user_nome.get().strip()
    credencial = credencial_entrada.get().strip()

    if not username or not credencial:
        status_label.configure(text="Por favor, preencha todos os campos", text_color="#FF5555")
        return

    if credencial in credenciais_validas:
        status_label.configure(text="Login realizado com sucesso!", text_color="#55FF55")
        botao_entrar.configure(state="disabled")
        janela.after(2000, iniciar_programa)
    else:
        status_label.configure(text="Credencial inválida. Tente novamente.", text_color="#FF5555")
        credencial_entrada.delete(0, 'end')

# Botão de login
botao_entrar = ctk.CTkButton(
    inner_frame,
    text="ENTRAR",
    command=verificar_credenciais,
    width=200,
    height=45,
    corner_radius=8,
    fg_color="white",
    hover_color="gray",
    text_color="black",
    font=("Helvetica", 15, "bold")
)
botao_entrar.pack(pady=(10, 30))

# Iniciar o loop principal
janela.mainloop()