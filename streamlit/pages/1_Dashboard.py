import os
import pickle
import json
import requests

import pandas as pd
import numpy as np
import streamlit as st

import mapa

st.set_page_config(
    page_title="Previsão de Trajetória de Táxi",
    page_icon="📈"
    
)

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

def last_clicked():
    coordinate = mapa.map_expander()
    if coordinate and 41.13835 < coordinate['lat'] < 41.18593 and -8.69128 < coordinate['lng'] < -8.55261:
        st.session_state['start_lat'] = coordinate['lat']
        st.session_state['start_long'] = coordinate['lng']


def initialize_session_state():
    if 'start_lat' not in st.session_state:
        st.session_state['start_lat'] = 41.1579

    if 'start_long' not in st.session_state:
        st.session_state['start_long'] = -8.6291

    if 'origin_call' not in st.session_state:
        st.session_state['origin_call'] = 2001.0

    if 'origin_stand' not in st.session_state:
         st.session_state['origin_stand'] = np.NaN

def create_ui():
    st.title("Projeto Previsão de Trajetória de Táxi")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            create_call_type_section()
        with col2:
            create_taxi_id_section()

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            create_origin_call_section()
        with col2:
            create_origin_stand_section()

    with st.container():
        col1, col2 = st.columns(2)
        create_start_coordinates_section()


def create_call_type_section():
    data = load_data()
    call_type = st.selectbox(label='Call Type:', options=data['call_type'], key='call_type')
    return call_type


def create_origin_call_section():
    data = load_data()
    call_type = st.session_state.get('call_type', '')
    if call_type == 'A':
        origin_call = st.selectbox(label='Origin Call:', options=data['origin_call'])
        st.session_state['origin_call'] = origin_call
    else:
        origin_call = st.selectbox(label='Origin Call', options=['Campo não Permitido'])
        st.session_state['origin_call'] = np.NaN
    return origin_call

def create_taxi_id_section():
    data = load_data()
    call_type = st.selectbox(label='Taxi Id:', options=data['taxi_id'], key='taxi_id')
    return call_type

def create_origin_stand_section():
    data = load_data()
    call_type = st.session_state.get('call_type', '')
    if call_type == 'B':
        origin_stand = st.selectbox(label='Origin Stand:', options=data['origin_stand'])
        st.session_state['origin_stand'] = origin_stand
    else:
        origin_stand = st.selectbox(label='Origin Stand:', options=['Campo não Permitido'])
        st.session_state['origin_stand'] = np.NaN
    return origin_stand


def create_start_coordinates_section():
    start_lat = st.number_input(label="Latitude Inicial", 
                                value=st.session_state['start_lat'], 
                                placeholder="Digite a Latitude", 
                                min_value=41.13835, 
                                max_value=41.18593, 
                                format="%.4f", 
                                step=0.001)

    start_long = st.number_input(label="Longitude Inicial", 
                                 value=st.session_state['start_long'], 
                                 placeholder="Digite a Longitude", 
                                 min_value=-8.69128, 
                                 max_value=-8.55261, 
                                 format="%.4f", 
                                 step=0.001)

    return start_lat, start_long


def main():
    initialize_session_state()
    data = load_data()
    create_ui()

    with st.expander(label='Ver mapa', expanded=True):
        last_clicked()

    if st.button(label= 'Previsão'):
        call_type = st.session_state.get('call_type')
        origin_call = st.session_state.get('origin_call')
        origin_stand = st.session_state.get('origin_stand')
        start_lat = st.session_state.get('start_lat')
        start_long = st.session_state.get('start_long')

        input_data = pd.DataFrame({
            'call_type': [call_type],
            'origin_call': [origin_call],
            'origin_stand': [origin_stand],
            'start_lat': [start_lat],
            'start_long': [start_long]
        })

        prediction = predict(input_data)
        st.dataframe(prediction)
        mapa.show_map(prediction)


if __name__ == "__main__":
    main()
