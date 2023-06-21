import tkinter as tk
from tkinter import ttk, filedialog
from logic import processar_arquivo
from pathlib import Path


def get_desktop_path():
    return str(Path.home() / "Desktop")


def processar_arquivo_gui():
    # Obter o caminho da área de trabalho
    desktop_path = get_desktop_path()

    # Abrir o seletor de arquivos com o diretório inicial configurado para a área de trabalho
    arquivo_csv = filedialog.askopenfilename(
        initialdir=desktop_path,
        filetypes=[('Arquivos CSV', '*.csv')]
    )

    if arquivo_csv:
        try:
            # Processar o arquivo CSV
            df = processar_arquivo(arquivo_csv)

            # Solicitar ao usuário o local para salvar a planilha corrigida
            output_file = filedialog.asksaveasfilename(
                initialdir=desktop_path,
                defaultextension='.csv',
                filetypes=[('Arquivos CSV', '*.csv')]
            )

            if output_file:
                # Salvar a planilha corrigida no formato UTF-8
                df.to_csv(output_file, encoding='utf-8', index=False)

            # Exibir uma mensagem de sucesso
            tk.messagebox.showinfo("Concluído!", "O arquivo foi corrigido com sucesso!")

            # Limpar a visualização atual
            limpar_visualizacao()

            # Exibir a pré-visualização da planilha corrigida
            for row in df.itertuples(index=False):
                preview_tree.insert('', tk.END, values=row)

            # Configurar as linhas de grade
            preview_tree.tag_configure("gridline", background="#d9d9d9")

        except ValueError as e:
            tk.messagebox.showerror("Erro", str(e))


def limpar_visualizacao():
    # Limpar a visualização da Treeview
    for item in preview_tree.get_children():
        preview_tree.delete(item)


# Criar a janela principal
window = tk.Tk()
window.title("Interface de Processamento de Arquivo")
window.geometry("500x400")
window.configure(background="#f0f0f0")
window.resizable(False, False)

# Criar o estilo para os botões
style = ttk.Style()
style.theme_use('clam')

style.configure(
    "TButton",
    padding=10,
    relief="flat",
    background="#51127f",
    foreground="white",
    font=("Arial", 12),
)
style.map(
    "TButton",
    relief=[('active', 'sunken')],
    background=[('active', "#410d66")]
)

# Criar o frame principal
frame = tk.Frame(window, bg="#f0f0f0")
frame.pack(padx=15, pady=15)

# Criar o botão para selecionar o arquivo
button_processar = ttk.Button(frame, text="Selecionar arquivo", command=processar_arquivo_gui, style="TButton")
button_processar.pack(side=tk.LEFT, padx=5)

# Criar o botão para limpar a visualização
button_limpar = ttk.Button(frame, text="Limpar visualização", command=limpar_visualizacao, style="TButton")
button_limpar.pack(side=tk.LEFT, padx=5)

# Criar a Treeview para a pré-visualização da planilha corrigida
preview_tree = ttk.Treeview(window, show="headings")
preview_tree["columns"] = ("column1", "column2")  # Substitua pelos nomes das colunas do seu DataFrame

# Configurar as colunas da Treeview
preview_tree.heading("column1", text="Números")
preview_tree.heading("column2", text="Nomes")
# Adicione mais linhas de código para configurar as colunas de acordo com seu DataFrame

preview_tree.pack(padx=20, pady=10)

created_by_label = ttk.Label(window, text="Criado por João Vitor Souza e Diego Machado")
created_by_label.pack(side=tk.BOTTOM, pady=10)

# Iniciar o loop da interface gráfica
window.mainloop()
