import streamlit as st
import pickle

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from helpers import Helpers
from sklearn.cluster import KMeans


import os.path
from os import path


def app():

    st.markdown("""
    ## Ubicación de centros de atención empleando clusterización con KMeans
    """)

    df = pd.read_csv(
        "/Bedu-C5/Bedu-C5/apps/data/incidentes-viales-c5-limpio.csv", sep="$", index_col=0)

    model_path = '/Bedu-C5/Bedu-C5/apps/kmeans_k50.sav'
    clasification_path = '/Bedu-C5/Bedu-C5/apps/kmeans_k50.csv'

    n_clusters = st.slider('No. de estaciones', min_value=1, max_value=50, value=50, step=1)
    max_iter = st.slider('Max. iteraciones', min_value=1000, max_value=100000, value=10000, step=100)

    @st.cache
    def wrapper_kmeans():
        k_means = KMeans(n_clusters=n_clusters, max_iter=max_iter)
        k_means.fit(df[['latitud', 'longitud']])
        return k_means

    if n_clusters==50 and path.exists(model_path):
        k_means = pickle.load(open(model_path, 'rb'))
    else:
        k_means = wrapper_kmeans()


    # Clasificaciones
    if n_clusters==50 and path.exists(clasification_path):
        clasificaciones =  pd.read_csv(clasification_path).values.ravel()
    else:
        clasificaciones = k_means.predict(df[['latitud', 'longitud']])
    

    # Encontrar las coordenadas reales más cercanas a los clusters
    centers =  k_means.cluster_centers_
    rep_points = pd.DataFrame(
    centers,
    columns=['latitude', 'longitude'])

    

    # Descargar el modelo
    st.markdown(Helpers.download_model(k_means), unsafe_allow_html=True)

    # Descargas datos 
    pd_clasificaciones = pd.DataFrame(clasificaciones)
    st.markdown(Helpers.get_table_download_link_csv(pd_clasificaciones), unsafe_allow_html=True) 

    # Gráficar en 2D usando seaborn
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title('Propuesta de centros de atención de accidentes vehiculares', pad=15)
    ax.set_xlabel('latitud')
    ax.set_ylabel('longitud')

    sns.scatterplot(df['longitud'], df['latitud'], ax=ax, hue=clasificaciones, palette='rainbow');

    sns.scatterplot(rep_points['longitude'], rep_points['latitude'], ax=ax, s=100,  color='black')
    # Desplegar el mapa en pantalla
    st.pyplot(fig)

    
    # Descargar coordenadas
    st.write("Coordenadas centros de atención propuestos")
    st.write(rep_points)

    

   # Graficando mapas
    st.markdown("""
    ## Ubicación de todos los centros de atención
    """)
    st.map(rep_points[['latitude','longitude']])

    # Opción de descarga
    st.markdown(Helpers.get_table_download_link_csv(rep_points), unsafe_allow_html=True) 


    # Detectando centro de atención más cercano
    st.markdown("""
    ## Úbica tu centro de atención más cercano
    """)

    user_long = st.number_input('Ingresa una latitud', min_value=-99.4, max_value=-98.9, value=-99.031232,format='%.6f')
    
    user_lat = st.number_input('Ingresa una longitud', min_value=19.000000, max_value=19.70000, step=0.000001, value=19.342259, format='%.6f')


    nearest_center_to_user = k_means.predict([[user_lat, user_long]])
    number_of_nearest_center_to_user = nearest_center_to_user[0]
    coord_of_nearest_center_to_user = centers[number_of_nearest_center_to_user]

    st.write(f"Partiendo de las coordenadas ({user_lat}, {user_long}), el centro de atención más cercano es el número {number_of_nearest_center_to_user} con coordenadas ({coord_of_nearest_center_to_user[0]:.6f}, {coord_of_nearest_center_to_user[1]:.6f})")


    df_nearest_center = pd.DataFrame([[coord_of_nearest_center_to_user[0], coord_of_nearest_center_to_user[1]], [user_lat, user_long]], columns=['lat', 'lon'])
    
    st.map(df_nearest_center)
