import pandas as pd
import streamlit as st
import requests  
from bs4 import BeautifulSoup
import time
import math
    

    #Path of the dataset
path = 'dataset/dataFull.csv'


#Set layout of the page for wide
st.set_page_config( layout='wide' )
    
    #load in cache the data 
@st.cache( allow_output_mutation=True )

#function for read csv
def get_data ( path ):
    data = pd.read_csv( path )
    return data


def create_tables(data):

    data = pd.read_csv("dataset/dadosFundaSchedule.csv")

    #Replace % for nothing
    data = df.apply(lambda x: x.str.replace('%',''))

    #Replace comma for nothing
    data = df.apply(lambda x: x.str.replace('.',''))


    #Replace comma for dot 
    data = data.apply(lambda x: x.str.replace(',','.'))


    #Transform the type OBJECT for FLOAT of the ROE and P/L columns
    data['ROE'] = data['ROE'].astype(float)
    data['P/L'] = data['P/L'].astype(float)
    data['Div.Yield'] = data['Div.Yield'].astype(float)
    data['Liq.2meses'] = data['Liq.2meses'].astype(float)
    data['Patrim. Líq'] = data['Patrim. Líq'].astype(float)



    #Create the a DF with 2 columns
    tableRoe = data[['Papel', 'ROE' ]]
    #Order for ROE and Right to Low 
    tableRoe = tableRoe.sort_values('ROE', ascending=True)
    #tableRoe
    #Save the CSV
    tableRoe.to_csv('dataset/rankingROE.csv', index=False)


    #Read CSV
    dfROE = pd.read_csv('dataset/rankingROE.csv')
    #Add the new columns pontosROE with INDEX
    dfROE['pontosROE'] = dfROE.index + 1
    #Save CSV
    dfROE.to_csv('dataset/rankingROE.csv', index=False)


    #Create the a DF with 2 columns
    tablePL = df[['Papel', 'P/L' ]]
    #Order for ROE and Right to Low 
    tablePL = tablePL.sort_values('P/L', ascending=False)
    #Save the CSV
    tablePL.to_csv('dataset/rankingPL.csv', index=False)


    #Read CSV
    dfPL = pd.read_csv('dataset/rankingPL.csv')
    #Add the new columns pontosPL with INDEX
    dfPL['pontosPL'] = dfPL.index + 1
    #Save CSV
    dfPL.to_csv('dataset/rankingPL.csv', index=False)


    #tableSoma = pd.concat([dfPL, dfROE], axis=1)
    tableSoma = pd.merge(dfPL, dfROE, on='Papel')
    tableSoma['soma'] = (tableSoma['pontosPL'] + tableSoma['pontosROE'])
    tableSoma = tableSoma.sort_values('soma', ascending=False)
    #tableSoma.to_csv('dataset/plroe-soma.csv', index=False)
    tableSoma.to_html('dataset/plroe-soma.html', index=False)


    tablePlRoe = pd.merge(tableSoma, df, on='Papel')

    tablePlRoe.to_csv('dataset/dataFull.csv', index=False)

    return None

def streamlit(data):

    
     #load data PL ROE
    data = get_data(path).sort_values('soma', ascending=False)

    #Title of the page
    st.title('Carteira de Joel Greenblatt - P/L x ROE - Bancos ')

    #SubTile of the page
    st.sidebar.header('O Padrão dos filtros são:')
    st.sidebar.markdown('0 < P/L < 15')
    st.sidebar.markdown('ROE > 10%')
    st.sidebar.markdown('DY > 5%')
    st.sidebar.markdown('Liq. 2 meses > 100.000')
    st.sidebar.markdown('Patr. Líquido > 0')
    st.sidebar.header('')
    

    #Header of the table PL / ROE
    st.header('Tabela PL / ROE')

    #Select the specific columns
    data = data[['Papel','P/L_x', 'ROE_x', 'Div.Yield', 'Liq.2meses', 'Patrim. Líq', 'PSR']]

    #Change the columns name
    data.columns = ['Ativos', 'P/L', 'ROE', 'DY', 'Liq. 2 meses', 'Patrim. Líquido', 'PSR' ]


    #Create filter of the Papers
    f_atributtes = st.sidebar.multiselect( 
        'Escolha o Ativo', data['Ativos'].unique())

    #Condition to filter for Papers not null
    if ( f_atributtes != [] ):
        data = data.loc[data['Ativos'].isin( f_atributtes )]
    else:
        #Condition to filter for Papers is null
        data = data.copy() 


    #Standard values
    plessencial = [0,15]

    #Filter Range PL
    #streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None)
    f_pl = st.sidebar.slider('Selecione o valor do P/L',  0, 50, (plessencial[0],plessencial[1]))

    if ( f_pl != [] ):
        data = data.loc[(data['P/L'] > f_pl[0]) & (data['P/L'] < f_pl[1])]
    else:
        data = data.loc[(data['P/L'].isin( f_pl ))]



    #Standard values
    roeessencial = [10,50]

    #Filter Range ROE
    #streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None)
    f_roe = st.sidebar.slider('Selecione o valor do ROE',  0, 50, (roeessencial[0],roeessencial[1]))

    if ( f_roe != [] ):
        data = data.loc[(data['ROE'] > f_roe[0]) & (data['ROE'] < f_roe[1])]
    else:
        data = data.loc[(data['ROE'].isin( f_roe ))]


     #Standard values
    dyessencial = [5,50]

    #Filter Range DY
    #streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None)
    f_dy = st.sidebar.slider('Selecione o valor do DY',  0, 50, (dyessencial[0],dyessencial[1]))

    if ( f_roe != [] ):
        data = data.loc[(data['DY'] > f_dy[0]) & (data['DY'] < f_dy[1])]
    else:
        data = data.loc[(data['DY'].isin( f_dy ))]



  

    #Standard values
    m2essencial = [100000,1000000]

    #Filter Range PL
    #streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None)
    f_2m = st.sidebar.slider('Selecione o valor do Liq. 2 meses',  10000, 10000, (m2essencial[0],m2essencial[1]))

    if ( f_2m != [] ):
        data = data.loc[(data['Liq. 2 meses'] > f_2m[0])]
    else:
        data = data.loc[(data['Liq. 2 meses'].isin( f_2m ))]


               #Standard values
    palessencial = [0,0]

    #Filter Range PL
    #streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None)
    f_pal = st.sidebar.slider('Selecione o valor do Patrim. Líquido',  0, 100000000, (palessencial[0],palessencial[1]))

    if ( f_pal != [] ):
        data = data.loc[(data['Patrim. Líquido'] > f_pal[0]) & (data['Patrim. Líquido'] > f_pal[1])]
    else:
        data = data.loc[(data['Patrim. Líquido'].isin( f_pal ))]


    #Show de data
    st.dataframe(data, width=1000, height=500)

    return None

if __name__ == "__main__":

    data = get_data ( path )

    streamlit(data)

