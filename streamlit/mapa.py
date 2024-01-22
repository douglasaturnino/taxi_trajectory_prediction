from itertools import count

import folium
import geopandas as gpd
import osmnx as ox
from streamlit_folium import folium_static, st_folium
import streamlit as st
from folium.plugins import MousePosition, MarkerCluster

def map_expander():
    # Definir o nome da cidade
    city_name = "Porto, Portugal"

    # Coordenadas do Porto, Portugal
    latitude_porto = 41.1579
    longitude_porto = -8.6291

    # Geocodificar a cidade para obter a geometria
    area = ox.geocode_to_gdf(city_name)
  

    # Criar um mapa centrado na geometria da cidade do Porto
    mymap = folium.Map(location=[latitude_porto, longitude_porto], zoom_start=13)

    # Adicionar a geometria da cidade do Porto ao mapa
    folium.GeoJson(area).add_to(mymap)

    # Adicionar o plugin MousePosition para destacar marcador e caminho sob o mouse
    MousePosition().add_to(mymap)

    folium.ClickForMarker().add_to(mymap)

    st.title('Mapa Interativo - Porto, Portugal')

    # call to render Folium map in Streamlit
    st_data = st_folium(mymap, use_container_width=True, return_on_hover=True)
    return st_data['last_clicked']
    
    
def show_map(data):
    # Criar um mapa usando folium
    mymap = folium.Map(location=[data['start_lat'].mean(), data['start_long'].mean()], zoom_start=13)
    # Adicionar marcadores para o início e o fim de cada trajetória com cores diferentes e numeração
    for i, (index, row) in zip(count(start=1), data.iterrows()):
        start_popup = f'"<b>Latitude inicial:</b> {row["start_lat"]}<br/><b>Longitude inicial:</b> {row["start_long"]}"'
        pred_popup = f'"<b>Latitude predita:</b> {row["pred_lat"]}<br/><b>Longtude predita:</b> {row["pred_long"]}"'

        start_marker = folium.Marker([row['start_lat'], row['start_long']], 
                                        popup=folium.Popup(start_popup, max_width=300),
                                        icon=folium.Icon(color='blue')).add_to(mymap)

        pred_marker = folium.Marker([row['pred_lat'],row['pred_long']], 
                                        popup=folium.Popup(pred_popup, max_width=300), 
                                        icon=folium.Icon(color='red')).add_to(mymap)

    # Adicionar o plugin MousePosition para destacar marcador e caminho sob o mouse
    MousePosition().add_to(mymap)
    
    # Adicionar o plugin MarkerCluster para agrupar marcadores
    MarkerCluster().add_to(mymap)
    folium_static(mymap)