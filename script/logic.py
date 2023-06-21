import pandas as pd
import re
from pathlib import Path
import unidecode


def get_desktop_path():
    return str(Path.home() / "Desktop")


def processar_arquivo(arquivo_csv):
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

        return df
    except Exception as e:
        raise ValueError(f"Ocorreu um erro ao processar o arquivo: {str(e)}")
