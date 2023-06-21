import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import re
from pathlib import Path
import unidecode

def get_desktop_path():
    return str(Path.home() / "Desktop")

def processar_arquivo():
    # Obter o caminho da área de trabalho
    desktop_path = get_desktop_path()
    
    # Abrir o seletor de arquivos com o diretório inicial configurado para a área de trabalho
    arquivo_csv = filedialog.askopenfilename(initialdir=desktop_path, filetypes=[('Arquivos CSV', '*.csv')])

    if arquivo_csv:
        try:
            # Ler o arquivo CSV
            df = pd.read_csv(arquivo_csv)
            
            # Inicializa o contador
            contador = 1

            # Itera pelas linhas da planilha, começando da linha 2
            for index, row in df.iterrows():
                if pd.isna(row['name']):  # Verifica se o campo da coluna name está vazio
                    row['name'] = f"Sem nome {contador}"  # Preenche com "Sem nome" + contador
                    contador += 1

            # Iterar sobre as linhas a partir da segunda linha
            for index, row in df.iloc[1:].iterrows():
                # Verificar se há campos vazios na linha
                if pd.isnull(row['number']):
                    # Excluir a linha inteira
                    df = df.drop(index)

            # Remove os caracteres especiais de todas as colunas mantendo as letras que tinham ascentos
            for coluna in df.columns:
                df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(str(x)))
                df[coluna] = df[coluna].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x)))
                
            # Verificar e adicionar "55" aos valores da coluna A que não começam com "55"
            df['number'] = df['number'].apply(lambda x: '55' + str(x) if not str(x).startswith('55') else str(x))
            
            # Verificar e remover o quinto dígito dos números de telefone
            for index, row in df.iterrows():
                numero_telefone = str(row['number'])
                ddd = int(numero_telefone[2:4])

                if ddd > 29 and len(numero_telefone) >= 5:
                    # Remover o quinto dígito
                    df.loc[index, 'number'] = numero_telefone[:4] + numero_telefone[5:]

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
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo: {str(e)}")

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
frame.pack(padx=20, pady=20)

# Criar o botão para selecionar o arquivo
button_processar = ttk.Button(frame, text="Selecionar arquivo CSV", command=processar_arquivo, style="TButton")
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
