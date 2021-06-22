import streamlit as st

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

    # Gráficar en 2D usando seaborn
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title('Propuesta de centros de atención de accidentes vehiculares', pad=15)
    ax.set_xlabel('latitud')
    ax.set_ylabel('longitud')
    sns.scatterplot(rep_points['latitude'], rep_points['longitude'], ax=ax)
    # Desplegar el mapa en pantalla
    st.pyplot(fig)

    # Desplegar coordenadas en mapa dinámico


   # Graficando mapas
    st.markdown("""
    # Encontrar la coordenada más cercana al cluster
    """)
    st.map(rep_points[['latitude','longitude']])

    # Opción de descarga
    st.markdown(Helpers.get_table_download_link_csv(rep_points), unsafe_allow_html=True) 
