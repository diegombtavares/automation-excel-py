import tkinter as tk
from tkinter import ttk, filedialog
import pandas
from auto.logic import processar_arquivo
from pathlib import Path


def get_desktop_path():
    return str(Path.home() / "Desktop")


def processar_arquivo_gui():
    # Obter o caminho da área de trabalho
    desktop_path = get_desktop_path()
    
    # Abrir o seletor de arquivos com o diretório inicial configurado para a área de trabalho
    arquivo_csv = filedialog.askopenfilename(initialdir=desktop_path, filetypes=[('Arquivos CSV', '*.csv')])

    if arquivo_csv:
        try:
            # Processar o arquivo CSV
            df = processar_arquivo(arquivo_csv)

            # Solicitar ao usuário o local para salvar a planilha corrigida
            output_file = filedialog.asksaveasfilename(initialdir=desktop_path, defaultextension='.csv', filetypes=[('Arquivos CSV', '*.csv')])

            if output_file:
                # Salvar a planilha corrigida no formato UTF-8
                df.to_csv(output_file, encoding='utf-8', index=False)

            # Exibir uma mensagem de sucesso
            tk.messagebox.showinfo("Concluído!", "O arquivo foi corrigido com sucesso!")

            # Exibir a pré-visualização da planilha corrigida
            preview_text.delete("1.0", tk.END)  # Limpar o conteúdo atual
            preview_text.insert(tk.END, df.to_string(index=False))
        except ValueError as e:
            tk.messagebox.showerror("Erro", str(e))


def limpar_visualizacao():
    preview_text.delete("1.0", tk.END)  # Limpar o conteúdo atual


# Criar a janela principal
window = tk.Tk()
window.title("Interface de Processamento de Arquivo")
window.geometry("500x400")
window.configure(background="#f0f0f0")
window.resizable(False, False)

# Criar o estilo para os botões
style = ttk.Style()
style.theme_use('clam')

style.configure("TButton",
                padding=10,
                relief="flat",
                background="#4caf50",
                foreground="white",
                font=("Arial", 12),
                )
style.map("TButton",
          relief=[('active', 'sunken')],
          background=[('active', "#45a049")]
          )

# Criar o frame principal
frame = tk.Frame(window, bg="#f0f0f0")
frame.pack(padx=15, pady=15)

# Criar o botão para selecionar o arquivo
button_processar = ttk.Button(frame, text="Selecionar arquivo CSV", command=processar_arquivo_gui, style="TButton")
button_processar.pack(side=tk.LEFT, padx=5)

# Criar o botão para limpar a visualização
button_limpar = ttk.Button(frame, text="Limpar visualização", command=limpar_visualizacao, style="TButton")
button_limpar.pack(side=tk.LEFT, padx=5)

# Criar a caixa de texto para a pré-visualização da planilha corrigida
preview_text = tk.Text(window, height=15, width=60)
preview_text.pack(padx=20, pady=10)

created_by_label = ttk.Label(window, text="Criado por João Vitor Souza e Diego Machado")
created_by_label.pack(side=tk.BOTTOM, pady=10)

# Iniciar o loop da interface gráfica
window.mainloop()
