import streamlit as st

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from helpers import Helpers
from sklearn.cluster import KMeans


def app():

    st.markdown("""
    ## Ubicación de centros de atención empleando clusterización con KMeans
    """)

    df = pd.read_csv(
        "/Bedu-C5/Bedu-C5/apps/data/incidentes-viales-c5-limpio.csv", sep="$", index_col=0)

    n_clusters = st.slider('No. de estaciones', min_value=1, max_value=50, value=10, step=1)
    max_iter = st.slider('Max. iteraciones', min_value=1000, max_value=100000, value=10000, step=100)

    @st.cache
    def wrapper_kmeans():
        k_means = KMeans(n_clusters=n_clusters, max_iter=max_iter)
        k_means.fit(df[['latitud', 'longitud']])
        return k_means

    k_means = wrapper_kmeans()
    
    # Encontrar las coordenadas reales más cercanos a los clusters
    centers =  k_means.cluster_centers_
    rep_points = pd.DataFrame(
    centers,
    columns=['latitude', 'longitude'])

    st.write(rep_points)

    # Clasificaciones
    clasificaciones = k_means.predict(df[['latitud', 'longitud']])

    # Gráficar en 2D usando seaborn
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title('Propuesta de centros de atención de accidentes vehiculares', pad=15)
    ax.set_xlabel('latitud')
    ax.set_ylabel('longitud')


    sns.scatterplot(df['latitud'], df['longitud'], ax=ax, hue=clasificaciones, palette='rainbow');

    sns.scatterplot(rep_points['longitude'], rep_points['latitude'], ax=ax, s=100,  color='black')
    # Desplegar el mapa en pantalla
    st.pyplot(fig)

    # Desplegar coordenadas en mapa dinámico
    

   # Graficando mapas
    st.markdown("""
    ## Ubincación de todos los centros de atención
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
