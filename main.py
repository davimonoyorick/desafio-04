
import pandas as pd               
import numpy as np                
import seaborn as sns             
import matplotlib.pyplot as plt  


# lendo o dataframe
df = pd.read_csv("Trilhas2B-Desafio 4  - Churn.csv")


#  Altere os nomes das colunas para letras minúsculas, utilizando a biblioteca pandas;
df.columns = df.columns.str.lower()  # Deixa todas as colunas em letras minúsculas
print(df.columns)


# corrigir os dados categóricos, : "Mas" para "Masculino", "Fem" para "Feminino" 
df['genero'] = df['genero'].replace({
    'M': 'Masculino',
    'Mas': 'Masculino',
    'F': 'Feminino',
    'Fem': 'Feminino'
})

#corrigir dados faltantes

print(df.isnull().sum()) # verificando quais colunas tem valores nulos
# Preencher valores ausentes em 'genero' com o valor mais frequente (moda)
df['genero'] = df['genero'].fillna(df['genero'].mode()[0])

# Preencher valores ausentes em 'salario anual' com a mediana (evita distorções de outliers)
df['salario anual'] = df['salario anual'].fillna(df['salario anual'].median())


#remoção de duplicatas

df = df.drop_duplicates()


# tratar outliers

numerical_cols = ['pontos', 'idade', 'bens', 'saldo na conta', 'produtos', 'salario anual']

for col in numerical_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    median = df[col].median()
    df[col] = np.where((df[col] < lower_bound) | (df[col] > upper_bound), median, df[col])


#exploração categórica com groupby()

# Analisar proporção de churn  por estado
grouped_estado = df.groupby('estado')['saiu'].value_counts(normalize=True).unstack()

# Analisar proporção de churn por gênero
grouped_genero = df.groupby('genero')['saiu'].value_counts(normalize=True).unstack()


# estatísticas descritivas de variáveis numéricas

print("Estatísticas descritivas:\n")
print(df[numerical_cols].describe())


# boxplot das variáveis numéricas


df[numerical_cols].boxplot(rot=45)
plt.title('Boxplot das variáveis numéricas')
plt.tight_layout()
plt.show()

#Boxplot com seaborn

sns.boxplot(data=df, x='salario anual')

plt.title('Boxplot do Salário Anual')
plt.xlabel('Salário Anual')
plt.show()


# gráfico de churn por estado


grouped_estado.plot(kind='bar', stacked=True)
plt.title('Proporção de Churn por Estado')
plt.ylabel('Proporção')
plt.xlabel('Estado')
plt.legend(title='Saiu')
plt.tight_layout()
plt.show()


# gráfico de churn por gênero


grouped_genero.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Proporção de Churn por Gênero')
plt.ylabel('Proporção')
plt.xlabel('Gênero')
plt.legend(title='Saiu')
plt.tight_layout()
plt.show()


# tamanho do dataframe df
print(f"Tamanho final dos dados após tratamento: {df.shape}")


#Apresente a média e a mediana do saldo na conta dos clientes abaixo de 40 anos;
clientes_jovens = df[df['idade'] < 40]
media_saldo = clientes_jovens['saldo na conta'].mean()
mediana_saldo = clientes_jovens['saldo na conta'].median()

print(f"Média do saldo na conta de clientes com idade < 40): R$ {media_saldo:.2f}\n\n")
print(f"Mediana do saldo na conta de clientes com idade < 40): R$ {mediana_saldo:.2f}\n\n")


#Apresente a média e a mediana do saldo na conta dos clientes acima de 40 anos;
clientes_acima_40 = df[df['idade'] > 40]


media_saldo = clientes_acima_40['saldo na conta'].mean()
mediana_saldo = clientes_acima_40['saldo na conta'].median()

print(f"Média do saldo na conta com idade menor que 40 anos: R$ {media_saldo:.2f}\n\n")
print(f"Mediana do saldo na conta com idade maior que 40 anos): R$ {mediana_saldo:.2f}\n\n")


#Apresente a média e a mediana do saldo na conta dos clientes que saíram e dos que permaneceram;
resumo = df.groupby('saiu')['saldo na conta'].agg(['mean', 'median'])

print(resumo)

#Dos que saíram, mostre qual é o público predominante (Masculino ou Feminino), a idade, o saldo na conta, patrimônio e os seus respectivos estados;

# Filtrar clientes que saíram
clientes_sairam = df[df['saiu'] == 1]

# Público predominante (gênero)
genero_predominante = clientes_sairam['genero'].mode()[0]

# Média da idade
media_idade = clientes_sairam['idade'].mean()

# Média do saldo na conta
media_saldo = clientes_sairam['saldo na conta'].mean()

# Média do patrimônio (bens)
media_bens = clientes_sairam['bens'].mean()

# Contagem por estado
contagem_estados = clientes_sairam['estado'].value_counts()

print(f"Gênero predominante dos que saíram: {genero_predominante}")
print(f"Média da idade: {media_idade} anos")
print(f"Média do saldo na conta: R$ {media_saldo}")
print(f"Média do patrimônio (bens): R$ {media_bens}")
print("\nContagem dos que saíram por estado:")
print(contagem_estados)

