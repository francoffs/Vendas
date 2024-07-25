from pathlib import Path
from datetime import date, datetime, timedelta

import streamlit as st
import pandas as pd

COMISSAO = 0.08
COLUNAS_ANALISE = ['filial', 'vendedor', 'produto', 'cliente_genero', 'forma_pagamento']
COLUHNAS_NUMERICAS = ['preco', 'comissão']
FUNCOES_AGG = {'soma': 'sum', 'contagem': 'count'}

df_vendas = pd.read_csv('vendas.csv', decimal=',', sep=';', index_col=0)
df_produtos = pd.read_csv('produtos.csv', decimal=',', sep=';', index_col=0)
df_filiais = pd.read_csv('filiais.csv', decimal=',', sep=';', index_col=0)

df_produtos = df_produtos.rename(columns={'nome': 'produto'})
df_vendas = pd.merge(left=df_vendas.reset_index(),
                     right=df_produtos[['produto', 'preco']],
                     on='produto',
                     how='left')
df_vendas = df_vendas.set_index('data')
df_vendas['comissão'] = df_vendas['preco']*COMISSAO

indice_dinamica = st.sidebar.multiselect('Selecione os índices:',
                       COLUNAS_ANALISE)
colunas_filtradas = [c for c in COLUNAS_ANALISE if not c in indice_dinamica]
coluna_dinamica = st.sidebar.multiselect('Selecione as colunas:',
                       colunas_filtradas)

valor_analise = st.sidebar.selectbox('Selecione o valor:',
                                     COLUHNAS_NUMERICAS)
metrica_analise = st.sidebar.selectbox('Selecione a métrica:',
                                     list(FUNCOES_AGG.keys()))
if len(indice_dinamica) > 0 and len(coluna_dinamica) > 0: 
    metrica = FUNCOES_AGG[metrica_analise]
    vendas_dinamica = pd.pivot_table(df_vendas,
                                     index=indice_dinamica,
                                     columns=coluna_dinamica,
                                     values=valor_analise,
                                     aggfunc=metrica)
    vendas_dinamica['TOTAL GERAL'] = vendas_dinamica.sum(axis=1)
    vendas_dinamica.loc['TOTAL GERAL'] = vendas_dinamica.sum(axis=0).to_list()
    st.dataframe(vendas_dinamica)

    
