from pathlib import Path

import streamlit as st
import pandas as pd

pasta_datasets = Path(__file__).parent
caminho_vendas = pasta_datasets / 'vendas.csv'

df_vendas = pd.read_csv(caminho_vendas, sep=';', decimal=',')

st.dataframe(df_vendas)

