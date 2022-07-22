import investpy as ip
from pytz import country_names
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Função para consultar as Ações
@st.cache
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(stock=stock, country=country, from_date=from_date, to_date=to_date, interval=interval)
    return df.head()

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

def plotCandleStick(df, acao='ticket'):
    tracel = {
        'x':df.index,
        'open':df.Open,
        'close':df.Close,
        'high':df.High,
        'low':df.Low,
        'type': 'candlestick',
        'name':acao,
        'showlegend':False

    }
    data = [tracel]
    layout = go.Layout()
    fig = go.Figure(data=data, layout=layout)
     
    return fig

# Captando as ações
pais_br = ['Brasil', 'Estados Unidos']
paises = ['brazil', 'united states']
intervalo = ['Daily', 'Weekly', 'Mounthy']
intervalo_br = ['Dia', 'Semana', 'Mês']
titulo = st.header('Gráfio de açoes')

# Consulta(query) das Açoes
dt_inicio = datetime.today() - timedelta(days=30)
dt_fim = datetime.today()


selecao_pais = st.sidebar.selectbox('Selecione o pais:', pais_br)
if selecao_pais == 'Brasil':
    selecao_pais = paises[0]
else:
    selecao_pais = paises[1]

acoes = ip.get_stocks_list(country=selecao_pais)

selecao_acoes = st.sidebar.selectbox('Escolha uma ação', acoes)
from_date = st.sidebar.date_input('De:',dt_inicio)
to_date = st.sidebar.date_input('De:', dt_fim)


seleca_intervalo = st.sidebar.selectbox('Selecione o Intervalo', intervalo_br)
if seleca_intervalo == 'Dia':
    seleca_intervalo = intervalo[0]
elif seleca_intervalo == 'Semana':
    seleca_intervalo = intervalo[1]
else:
    seleca_intervalo = intervalo[2]

carregar_dados = st.sidebar.checkbox('Carregar Dados')

format_date(from_date)
format_date(to_date)

grafico_candle = st.empty()
grafico_line = st.empty()

if from_date > to_date:
    st.sidebar.error('Data de inicio maior do que a data final')
else:
    df = consultar_acao(selecao_acoes, selecao_pais, format_date(dt_inicio), format_date(dt_fim), seleca_intervalo)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)

        if carregar_dados:
            st.subheader('Dados')
            dados = st.dataframe(df)
    except Exception as e:
        st.error(e)
