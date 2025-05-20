import pandas as pd  

dados = df = pd.read_csv("Trilhas2B-Desafio 4  - Churn.csv")

#print(dados.shape)

#print(dados.columns)

#print(dados.info())

print(dados.isnull().sum())
