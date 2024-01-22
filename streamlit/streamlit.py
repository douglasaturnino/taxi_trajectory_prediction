import os
import pickle
import json
import requests

import pandas as pd
import numpy as np
import streamlit as st

import mapa


@st.cache_data 
def load_data():
    home_path = os.path.join(os.getcwd(), 'dataset', 'valores_unicos.pkl')
    data = pickle.load(open(home_path, 'rb'))
    return data

def predict(data):
    url = os.getenv('WEB_URL', 'http://localhost:5000/predict')
    header = {'Content-type': 'application/json'}
    data = json.dumps(data.to_dict(orient='records'))
    response = requests.get(url, data=data, headers=header)
    
    return pd.DataFrame(response.json(), columns=response.json()[0].keys())


if 'start_lat' not in st.session_state:
    st.session_state['start_lat'] = 41.1579

if 'start_long' not in st.session_state:
    st.session_state['start_long'] = -8.6291

data = load_data()
st.title("Projeto Previsão de trajetória de táxi")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        call_type = st.selectbox(label='Call Type:', options=data['call_type'])

    with col2:
        if call_type == 'A':
            origin_call = st.selectbox(label='Origin Call:', options=data['origin_call'])
        else:
            origin_call = st.selectbox(label='Origin Call', options=['Campo não Permitido'])
            origin_call = np.NaN

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        if call_type == 'B':
            origin_stand = st.selectbox(label='Origin Stand:', options=data['origin_stand'])
        else:
            origin_stand = st.selectbox(label='Origin Stand:', options=['Campo não Permitido'])
            origin_stand = np.NaN

    with col2:
        taxi_id = st.selectbox(label='Taxi Id:', options=data['taxi_id'])


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        start_lat = st.number_input(label="Latitude Inicial", value=st.session_state['start_lat'], placeholder="Digite a Latitude", min_value=41.13835, max_value=41.18593, format="%.5f", step=0.001)

    with col2:
        start_long = st.number_input(label="Longitude Inicial", value=st.session_state['start_long'], placeholder="Digite a Longitude", min_value=-8.69128, max_value=-8.55261, format="%.5f", step=0.001)

with st.expander("Ver mapa"):
    mapa.map_expander()


if st.button(label= 'Previsão'):
    data = pd.DataFrame(
        {
            'call_type': [call_type],
            'origin_call': [origin_call],
            'origin_stand': [origin_stand],
            'start_lat': [start_lat],
            'start_long': [start_long]

        })

    data = predict(data)
    st.dataframe(data)
    mapa.show_map(data)

