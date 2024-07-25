from pathlib import Path
from datetime import date, datetime, timedelta

import streamlit as st
import pandas as pd

COMISSAO = 0.08

df_vendas = pd.read_csv('vendas.csv', decimal=',', sep=';', index_col=0, parse_dates=True)
df_produtos = pd.read_csv('produtos.csv', decimal=',', sep=';', index_col=0, parse_dates=True)
df_filiais = pd.read_csv('filiais.csv', decimal=',', sep=';', index_col=0, parse_dates=True)

df_produtos = df_produtos.rename(columns={'nome': 'produto'})
df_vendas = df_vendas.reset_index()
df_vendas = pd.merge(left=df_vendas, 
                     right=df_produtos[['preco', 'produto']],
                     on='produto',
                     how='left')

df_vendas = df_vendas.set_index('data')
df_vendas['comissão'] = df_vendas['preco']*COMISSAO

data_default = df_vendas.index.date.max()
data_inicio = st.sidebar.date_input('Data Inicial', data_default - timedelta(days=365))
data_final = st.sidebar.date_input('Data Final', data_default)

df_vendas_cortado = df_vendas[(df_vendas.index.date >= data_inicio) & (df_vendas.index.date < data_final + timedelta(days=1))]

st.markdown('# Números Gerais')
col1, col2 = st.columns(2)

valor_vendas = df_vendas_cortado['preco'].sum()
valor_vendas = f"R$ {valor_vendas:.2f}"
col1.metric('Valor das vendas no período', valor_vendas)

col2.metric('Quantidade de vendas no período', df_vendas_cortado['preco'].count())

st.divider()

principal_filial = df_vendas_cortado['filial'].value_counts().index[0]
st.markdown(f'# Principal Filial: {principal_filial}')
col21, col22 = st.columns(2)
valor_vendas = df_vendas_cortado[df_vendas_cortado['filial'] == principal_filial]['preco'].sum()
valor_vendas = f"R$ {valor_vendas:.2f}"
quantidade_vendas = df_vendas_cortado[df_vendas_cortado['filial'] == principal_filial]['preco'].count()
col21.metric('Valor de vendas no período', valor_vendas)
col22.metric('Quantidade de vendas no período', quantidade_vendas)

st.divider()


principal_vendedor = df_vendas_cortado['vendedor'].value_counts().index[0]
st.markdown(f'# Principal Vendedor: {principal_vendedor}')
col31, col32 = st.columns(2)
valor_vendas = df_vendas_cortado[df_vendas_cortado['vendedor'] == principal_vendedor]['preco'].sum()
valor_vendas = f"R$ {valor_vendas:.2f}"
valor_comissao = df_vendas_cortado[df_vendas_cortado['vendedor'] == principal_vendedor]['comissão'].sum()
valor_comissao = f'R$ {valor_comissao:.2f}'

col31.metric('Valor de vendas no período', valor_vendas)
col32.metric('Comissão no período', valor_comissao)