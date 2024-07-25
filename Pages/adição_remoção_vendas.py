from pathlib import Path
from datetime import datetime


import streamlit as st
import pandas as pd

from utilidades import leitura_de_dados

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

df_filiais['cidade/estado'] = df_filiais['cidade'] + "/" + df_filiais['estado']
cidades_filiais = df_filiais['cidade/estado'].to_list()


st.sidebar.markdown('## Adição de Vendas')
filial_selecionada = st.sidebar.selectbox('Selecione a filial',
                         cidades_filiais)
vendedores =  df_filiais.loc[df_filiais['cidade/estado'] == filial_selecionada, 'vendedores'].iloc[0]
vendedores = vendedores.strip('][]').replace("'", '').split(', ')
vendedor_selecionado = st.sidebar.selectbox('Selecione o vendedor', 
                                            vendedores)

produtos = df_produtos['nome'].to_list()
produto_selecionado = st.sidebar.selectbox('Selecione o produto:',
                                           produtos)
nome_cliente = st.sidebar.text_input('Nome do Cliente')
genero_selecionado = st.sidebar.selectbox('Gênero', 
                                          ['masculino', 'feminino'])
forma_pagamento = st.sidebar.selectbox('Forma de pagamento', 
                                          ['pix', 'boleto', 'débito', 'cartão'])
adicionar_venda = st.sidebar.button('Adicionar venda')
if adicionar_venda:
    lista_adicionar = [df_vendas['id_venda'].max() + 1,
                       filial_selecionada.split('/'[0]),
                       vendedor_selecionado,
                       produto_selecionado,
                       nome_cliente,
                       genero_selecionado, 
                       forma_pagamento
                       ]
    hora_adicionar = datetime.now()
    df_vendas.loc[hora_adicionar] = lista_adicionar
    caminho_datasets = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_datasets / 'vendas.csv', decimal=',', sep=';')
    

st.sidebar.markdown('## Excluir')
id_remoção = st.sidebar.number_input('ID a ser removido:',
                                     0,
                                     df_vendas['id_venda'].max())
                      
remover_venda = st.sidebar.button('Remover venda')
if remover_venda:
    df_vendas = df_vendas[df_vendas['id_venda'] != id_remoção]
    caminho_datasets = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_datasets / 'vendas.csv', decimal=',', sep=';')
    st.session_state['dados']['df_vendas'] = df_vendas

st.dataframe(df_vendas, height=800)
