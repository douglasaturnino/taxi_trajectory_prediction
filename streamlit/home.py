import os
import ast
import json
from itertools import count

import pandas as pd
import requests
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from streamlit_folium import folium_static
import streamlit as st


st.title("Bem vindo ao projeto Previsão de trajetória de táxi")

@st.cache_data 
def load_data():
    home_path = os.path.join(os.getcwd(), 'dataset', 'test.csv')
    data = pd.read_csv(home_path)
    return data

def predict(data):
    url = os.getenv('WEB_URL')
    header = {'Content-type': 'application/json'}
    data = json.dumps(data.to_dict(orient='records'))
    response = requests.get(url, data=data, headers=header)
    return pd.DataFrame(response.json(), columns=response.json()[0].keys())
    
def show_map(data):
    # Criar um mapa usando folium
    mymap = folium.Map(location=[data['start_long'].mean(), data['start_lat'].mean()], zoom_start=10)
    # Adicionar marcadores para o início e o fim de cada trajetória com cores diferentes e numeração
    for i, (index, row) in zip(count(start=1), data.iterrows()):
        start_popup = f'Start: {i}<br>Trip ID: {row["trip_id"]}'
        end_popup = f'pred: {i}<br>Trip ID: {row["trip_id"]}'

        start_marker = folium.Marker([row['start_long'], row['start_lat']], 
                                        popup=folium.Popup(start_popup, max_width=300),
                                        icon=folium.Icon(color='blue')).add_to(mymap)

        pred_marker = folium.Marker([row['pred_long'], row['pred_lat']], 
                                        popup=folium.Popup(start_popup, max_width=300), 
                                        icon=folium.Icon(color='red')).add_to(mymap)

        # Converter a string polyline para uma lista de coordenadas e inverter a ordem
        polyline_list = [[coord[1], coord[0]] for coord in ast.literal_eval(row['polyline'])]
        folium.PolyLine(locations=polyline_list, color="blue", weight=2.5, opacity=1).add_to(mymap)

    # Adicionar o plugin MousePosition para destacar marcador e caminho sob o mouse
    MousePosition().add_to(mymap)
    # Adicionar o plugin MarkerCluster para agrupar marcadores
    MarkerCluster().add_to(mymap)

    folium_static(mymap)

def coordinates(data):
    start_lat = 0 
    start_long = 1
    data["start_lat"] = extract_coordinates(data, start_lat)
    data["start_long"] = extract_coordinates(data, start_long)

    # Change Data Types
    data["start_lat"] = data["start_lat"].astype(float)
    data["start_long"] = data["start_long"].astype(float)

    return data

def extract_coordinates(df, coordinates):
    lista=list()
    for i in range(0,len(df["polyline"])):
        if df["polyline"][i] == '[]':
            ax=0
        else:
            ax = df["polyline"][i].split(',')[coordinates].strip('[]')
        lista.append(ax)

    return lista

if __name__ == "__main__":

    data = load_data()

    filter_ = st.multiselect(label='Selecione o id taxi:', options=data['TAXI_ID'].sort_values().unique(), default=[20000005])

    linhas_seleciondas = data.loc[data['TAXI_ID'].isin(filter_)]

    st.dataframe(linhas_seleciondas)

    if st.button(label='Previsão'):
        data = predict(linhas_seleciondas)
        data = coordinates(data)
        data_aux = data[['trip_id', 'taxi_id', 'start_lat', 'start_long', 'pred_lat', 'pred_long']]
        st.dataframe(data_aux)
        show_map(data)
    