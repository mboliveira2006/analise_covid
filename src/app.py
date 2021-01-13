import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache
def carregadados(caminho):
    dados = pd.read_csv(caminho)
    return dados


def grafico_comparativo(dados_2019, dados_2020, causa, uf='BRASIL'):

    uf = str(uf).upper()

    if uf == 'BRASIL' and causa !='':
        total_2019 = dados_2019.groupby(['tipo_doenca'])['total'].sum()
        total_2020 = dados_2020.groupby(['tipo_doenca'])['total'].sum()
        lista = [total_2019.loc[causa], total_2020.loc[causa]]

    elif causa != '' and uf != '':
        if causa =='COVID':
            total_2019 = 0
        else:
            total_2019 = dados_2019.groupby(['uf','tipo_doenca'])['total'].sum()
            
        total_2020 = dados_2020.groupby(['uf','tipo_doenca'])['total'].sum()
        
        lista = [total_2019.loc[uf, causa], total_2020.loc[uf, causa]]
    
    elif causa == '' and uf != '':
        total_2019 = dados_2019.groupby(['uf'])['total'].sum()
        total_2020 = dados_2020.groupby(['uf'])['total'].sum()
        
        lista = [total_2019.loc[uf.upper()], total_2020.loc[uf.upper()]]

    dados = pd.DataFrame({'Total': lista,'Ano': [2019,2020]})

    fig, ax = plt.subplots()
    ax =  sns.barplot(x ='Ano', y ='Total', data = dados)
    ax.set_title(f'Óbitos por {causa} - {uf}')
    return fig


def main():
    
    obitos2019 = carregadados('dados/obitos-2019.csv')
    obitos2020 = carregadados('dados/obitos-2020.csv')
    tipo_doenca = obitos2020['tipo_doenca'].unique()
    tipo_estado = np.append(obitos2020['uf'].unique(),'BRASIL')

    st.title('Análise de óbitos 2019-2020')
    st.markdown('Este trabalho analisa dados dos **óbitos 2019-2020**')
    
    opcao_doenca = st.sidebar.selectbox('Selecione o tipo da doença', tipo_doenca)
    opcao_estado = st.sidebar.selectbox('Selecione o estado', tipo_estado)
    
    figura = grafico_comparativo(obitos2019, obitos2020, opcao_doenca,opcao_estado)
    
    st.pyplot(figura)

    
    
    #st.dataframe(obitos2019)
    #st.text("Minha aplicação")




if __name__ == '__main__':
    main()
