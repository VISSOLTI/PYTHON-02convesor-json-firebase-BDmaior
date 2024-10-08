import json
import pandas as pd
import numpy as np

df = pd.read_excel("firebase.xlsx")

# Remover - da coluna A
df['A'] = df['A'].str.replace('[-]', '', regex=True)
df['A'] = df['A'].str.rstrip()

# Converter colunas de data para strings

# Converter todas as colunas para string
df = df.astype(str)
for col in df.columns:
    if pd.api.types.is_datetime64_any_dtype(df[col]):
        df[col] = df[col].dt.strftime('%Y-%m-%d')  # Ajustar o formato da data conforme necessário

# Converter para lista de listas
lista_de_listas = df.values.tolist()


# Criando um DataFrame
df = pd.DataFrame(lista_de_listas, columns=['A','B','C','D','E','F','G','H',
                                            'I','J','K','L','M','N','O','P',
                                            'Q','R','S','T','U','V','W','X','Y','Z',
                                            'AA','AB','AC','AD','AE','AF','AG','AH',
                                            'AI','AJ','AK','AL','AM','AN','AO','AP',
                                            'AQ','AR','AS','AT'])


# ACRESCENTANDO R$
columns_to_modify = ['G', 'H', 'I', 'J', 'K', 'AS', 'AE', 'AN', 'AT']
for col in columns_to_modify:
    df[col] = df[col].apply(lambda x: pd.to_numeric(x, errors='coerce')).apply(lambda x: 'R$ {:,.2f}'.format(x).replace("nan", "0"))




columns_SEM_EXPOSICAO = ['A','B','C','D','E','F','G','H',
                            'I','J','K','L','M','N','O','P',
                            'Q','R','S','T','U','V','W','X','Y','Z',
                            'AA','AB','AC','AD','AE','AF','AG','AH',
                            'AI','AJ','AK','AL','AM','AN','AO','AP',
                            'AQ','AR','AS','AT']
for col in columns_SEM_EXPOSICAO:
    df[col] = df[col].replace("nan", "-")

print(df)
#SUBISTITUINDO . POR ,
columns_to_modify = ['G', 'H', 'J', 'K', 'AE', 'AT']
for col in columns_to_modify:
    df[col] = df[col].apply(lambda x: str(x).replace('.', ','))

# Convertendo as colunas 'E', 'F' e 'AP' para o tipo datetime e formatando
df['E'] = pd.to_datetime(df['E'], format='%Y-%m-%d').dt.strftime('%d/%m/%Y').replace("nan", "-")
df['F'] = pd.to_datetime(df['F'], format='%Y-%m-%d').dt.strftime('%d/%m/%Y')
df['AP'] = pd.to_datetime(df['AP'], format='%Y-%m-%d').dt.strftime('%d/%m/%Y')
# tirando os 00:00:00
df['AQ'] = df['AQ'].str.replace(' 00:00:00', '')
df['AQ'] = pd.to_datetime(df['AQ'], format='%Y-%m-%d', errors='coerce')
df['AQ'] = df['AQ'].dt.strftime('%d/%m/%Y')


# Definindo o CNPJ/CPF como índice
df.set_index('A', inplace=True)

dicionario = df.groupby('A').apply(lambda x: x.to_dict('records')).to_dict()

# Função para converter NaN para uma string específica
def nan_to_string(val):
    if isinstance(val, float) and np.isnan(val):
        return "N/A"
    else:
        return val

# Aplicar a função a todos os valores do dicionário
for chave, lista_de_registros in dicionario.items():
    for registro in lista_de_registros:
        for k, v in registro.items():
            registro[k] = nan_to_string(v)

# Converter para JSON
json_data = json.dumps(dicionario, indent=4)

#print(json_data)

# Salvando em um arquivo (opcional)
with open('firebase.json', 'w') as f:
     f.write(json_data)



#A,	B,	C,	D,	E,	F,	G,	H,	I,	J,	K,	L,	M,	N,	O,	P,	Q,	R,	S

#056.122.507/0001-72


#
# 2024-09-19 00:00:00
# 2024-09-19 00:00:00
# 2024-09-20 00:00:00
# 2024-09-16 00:00:00
# 2024-09-23 00:00:00
# 2024-09-23 00:00:00
# 2024-09-16 00:00:00
# 2024-09-18 00:00:00