import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt   
from pylab import *


#Configura o formato de exibiçao dos valores float
pd.set_option('display.float_format', '{:.2f}'.format)

df = pd.read_csv('dataset.csv')
df = df [['ID_Pedido',	'Data_Pedido',	'ID_Cliente',	'Segmento','Pais',	'Cidade',	'Estado',	
                  'ID_Produto',	'Categoria',	'SubCategoria',	'Valor_Venda']]

'''
 Pergunta de Negócio 1:
 Qual Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies'?
'''
# Cidade com maior valor de vendas na categoria Office Supplies(para saber outras categorias altere o item em questao)
OficeSupplies = df[df['Categoria']=='Office Supplies']
CitySelles = OficeSupplies.groupby('Cidade')['Valor_Venda'].sum()
top_city = CitySelles.idxmax()
print(top_city)

'''
 Pergunta de Negócio 2:
 Qual o Total de Vendas Por Data do Pedido?
 Demonstre o resultado através de um gráfico de barras.
'''

# Converter 'Data_Pedido' para datetime
df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'])

# Soma do valor de venda por data
vendas = df.groupby ('Data_Pedido')['Valor_Venda'].sum()

# Criar um gráfico de barras
plt.figure(figsize=(15, 6))
plt.bar(vendas.index, vendas.values, color='blue')

# Adicionar rótulos e título
plt.xlabel('Data do Pedido')
plt.ylabel('Valor de Vendas')
plt.title('Vendas Diárias')
plt.legend()

# Mostrar o gráfico
plt.show()

'''
 Pergunta de Negócio 3:
 Qual o Total de Vendas por Estado?
 emonstre o resultado através de um gráfico de barras.
'''

# Soma do valor de venda por estado
totalVenda = df.groupby('Estado')['Valor_Venda'].sum()

# Criar um gráfico de barras
plt.figure(figsize=(15, 8))
plt.bar(totalVenda.index, totalVenda.values, color='r')

# Adicionar rótulos e título
plt.xlabel('Estado')
plt.ylabel('Valor de Vendas')
plt.title('Vendas por Estado')

# Melhorar a formatação das datas no eixo x
plt.xticks(rotation=90)
plt.tight_layout()

# Mostrar o gráfico
plt.show()

'''
 Pergunta de Negócio 4:
 Quais São as 10 Cidades com Maior Total de Vendas?
 Demonstre o resultado através de um gráfico de barras
'''

# Soma do valor de venda por cidade e ordena os 10 primeiros do maior para o menor
cityVendas = df.groupby('Cidade')['Valor_Venda'].sum()
cityVendas = cityVendas.sort_values(ascending=False)
print(cityVendas.head(10))

# Criar um gráfico de barras
plt.figure(figsize=(15, 8))
plt.bar(cityVendas.head(10).index, cityVendas.head(10).values, color='r')
plt.xlabel('Cidade')
plt.ylabel('Valor de Vendas')
plt.title('Vendas por Cidade')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

'''
 Pergunta de Negócio 5:
 Qual Segmento Teve o Maior Total de Vendas?
 Demonstre o resultado através de um gráfico de pizza.
'''

# Soma o valor de venda por segmento
segmentovenda = df.groupby('Segmento')['Valor_Venda'].sum()
segmentovenda = segmentovenda.sort_values(ascending=True)
print(segmentovenda)

# Extrai os valores e rótulos
fatias = segmentovenda.values
labels = segmentovenda.index

# Configura o tamanho do gráfico
plt.figure(figsize=(10, 6))

# cria um grafico de pizza 
# "autopct='%1.1f%%" Usado para mostrar a porcentagem de cada fatia
plt.pie(fatias, labels=labels, autopct='%1.1f%%', startangle=90)

# Adiciona o título
plt.title('Vendas por Segmento')
plt.show()

'''
 Pergunta de Negócio 6 (Desafio):
 Qual o Total de Vendas Por Segmento e Por Ano?
'''

df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'])
#Cria uma nova coluna no dataframe com o ano do pedido
df['Ano'] = df['Data_Pedido'].dt.year

#Agrupa o ano e o segmento e soma os valores de venda
vendasAnoSegmento = df.groupby(['Ano', 'Segmento'])['Valor_Venda'].sum()

#imprime o resultado
print(vendasAnoSegmento)

'''
 Pergunta de Negócio 7 (Desafio):
 Os gestores da empresa estão considerando conceder diferentes faixas de descontos e gostariam de fazer uma simulação com base na regra abaixo:

 Se o Valor_Venda for maior que 1000 recebe 15% de desconto.
 Se o Valor_Venda for menor que 1000 recebe 10% de desconto.
 Quantas Vendas Receberiam 15% de Desconto?
'''

# Cria uma coluna desconto no data frame e aplica uma função lambda para calcular o desconto
df['desconto'] = df['Valor_Venda'].apply(lambda x: x *0.1 if x > 1000 else x * 0.15)

# Cria um comparador booleano para verificar se o desconto é igual a 15% do valor da venda
vendasDesconto15 = (df['desconto'] == df['Valor_Venda'] * 0.15).sum()
print(f' Numero de vendas com 15% de desconto: {vendasDesconto15}')

'''
 Pergunta de Negócio 8 (Desafio):
 Considere Que a Empresa Decida Conceder o Desconto de 15% do Item Anterior. Qual Seria a Média do Valor de Venda Antes e Depois do Desconto?
'''

df['desconto'] = df['Valor_Venda'].apply(lambda x: x *0.15)
vendasmedia = df['Valor_Venda'].mean()
df['Venda_Desconto'] = df['Valor_Venda'] - df['desconto']
vendaDesconto = df['Venda_Desconto'].mean()
print(f'Valor medio das vendas: {vendasmedia:.2f} | Valor medio após desconto: {vendaDesconto:.2f}')

'''
 Pergunta de Negócio 9 (Desafio):
 Qual o Média de Vendas Por Segmento, Por Ano e Por Mês?
 Demonstre o resultado através de gráfico de linha.
'''

df['Mes'] = df['Data_Pedido'].dt.month
mediaVendaSegmento = df.groupby(['Ano', 'Mes', 'Segmento'])['Valor_Venda'].agg([np.sum, np.mean, np.median])
anos = mediaVendaSegmento.index.get_level_values(0)
meses = mediaVendaSegmento.index.get_level_values(1)
segmentos = mediaVendaSegmento.index.get_level_values(2)
print(mediaVendaSegmento)

plt.figure(figsize=(10, 8))
fig1 = sns.relplot(kind = 'line', data = mediaVendaSegmento, x = meses, y = 'mean', hue = segmentos, col = anos, col_wrap = 2)
plt.show()


'''
 Pergunta de Negócio 10 (Desafio):
 Qual o Total de Vendas Por Categoria e SubCategoria, Considerando Somente as Top 12 SubCategorias
 Demonstre tudo através de um único gráfico.
'''

totalcategoria = df.groupby('Categoria')['Valor_Venda'].sum()
totalcategoria = totalcategoria.sort_values(ascending=False)
totalsubcategoria = df.groupby('SubCategoria')['Valor_Venda'].sum()
totalsubcategoria = totalsubcategoria.sort_values(ascending=False)
subtop12 = totalsubcategoria.head(12)

grupCategorias = totalcategoria
top_12_subcategorias = subtop12

# Junta os dados das categorias e subcategorias
dadoscombinados = grupCategorias.append(top_12_subcategorias)

# Mapear os rótulos das barras para diferenciar categorias e subcategorias
combined_labels = [f'Cat: {categoria}' for categoria in grupCategorias.index] + [f'Sub: {sub}' for sub in top_12_subcategorias.index]
combined_values = dadoscombinados.values

# Configurar o gráfico
plt.figure(figsize=(15, 8))
bar_width = 0.35
index = np.arange(len(combined_labels))

# seta diferentes cores para os elementos diferentes
colors = ['b'] * len(grupCategorias) + ['g'] * len(top_12_subcategorias)


plt.bar(index, combined_values, bar_width, color= colors, label='Vendas')
plt.xlabel('Categorias e Subcategorias')
plt.ylabel('Valor de Vendas')
plt.title('Top 10 Categorias e Top 12 Subcategorias')
plt.xticks(index, combined_labels, rotation=90)
plt.tight_layout()
plt.show()