import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle

import os.path
from os import path

from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

from helpers import Helpers

def app():

    st.markdown("""
    ## Clusterización de coordenadas empleando DBScan
    """)

    df = pd.read_csv(
        "/Bedu-C5/Bedu-C5/apps/data/incidentes-viales-c5-limpio.csv", sep="$", index_col=0)

    km = st.slider('Radio en kilometros', min_value=0.1, max_value=5.0, value=0.25, step=0.1)
    min_samples = st.slider('Epsilon (num. vecinos)', min_value=1, max_value=10, value=3, step=1)

    
    model_path = '/Bedu-C5/Bedu-C5/apps/dbscan_r250m_ep4.sav'
    centroids_model_path = '/Bedu-C5/Bedu-C5/apps/dbscan_r250m_ep4.csv'

    #is_fit = path.exists(model_path) 
    #st.write(f"Cargando modelo entreado: {is_fit}")

    @st.cache
    def stremlit_dbscan(df, km=km, min_samples=min_samples):    
        coords = df[['latitud', 'longitud']].values
        kms_per_radian = 6371.0088
        epsilon = km / kms_per_radian

        if km==0.25 and min_samples==3:
            if path.exists(model_path):
                db = pickle.load(open(model_path, 'rb'))
            else:
                db = DBSCAN(eps=epsilon, min_samples=min_samples, algorithm='ball_tree',
                        metric='haversine').fit(np.radians(coords))
                pickle.dump(db, open(model_path, 'wb'))
        else:
            db = DBSCAN(eps=epsilon, min_samples=min_samples, algorithm='ball_tree',
                        metric='haversine').fit(np.radians(coords))        

        cluster_labels = db.labels_
        num_clusters = len(set(cluster_labels))  # Number of cluster with no noise
        # num_clusters = len(set(labels)) - (1 if -1 in labels else 0) # Number of cluster with noise
        clusters = pd.Series([coords[cluster_labels == n]
                         for n in range(num_clusters)])
        return cluster_labels, num_clusters, clusters, db


    cluster_labels, num_clusters, clusters, db = stremlit_dbscan(df)

    st.markdown(Helpers.download_model(db), unsafe_allow_html=True)

    st.write(f'Reducción de {len(df)} a {num_clusters} coordenadas')

    st.markdown("""
    ### Encontrar la coordenada más cercana al cluster
    """)

    
    def get_centermost_point(cluster):
        centroid = (MultiPoint(cluster).centroid.x,
                    MultiPoint(cluster).centroid.y)
        centermost_point = min(
            cluster, key=lambda point: great_circle(point, centroid).m)
        return tuple(centermost_point)

    @st.cache
    def wrapper_cache_center_most_points():
        centermost_points = clusters[:len(clusters)-1].map(get_centermost_point)
        lats, lons = zip(*centermost_points)
        rep_points = pd.DataFrame({'latitude': lats, 'longitude': lons})
        return rep_points


    # Encontrar las coordenadas reales más cercanos a los clusters
    if km==0.25 and min_samples==3 and path.exists(centroids_model_path):
        rep_points = pd.read_csv(centroids_model_path)
    else:
        rep_points = wrapper_cache_center_most_points()

    # Gráficar en 2D usando seaborn
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title('Locación de cluster', pad=15)
    ax.set_xlabel('latitud')
    ax.set_ylabel('longitud')
    sns.scatterplot(rep_points['longitude'], rep_points['latitude'], ax=ax)
    # Desplegar el mapa en pantalla
    st.pyplot(fig)

    # Desplegar coordenadas en mapa dinámico


   # Graficando mapas
    st.markdown("""
    ### Encontrar la coordenada más cercana al cluster
    """)
    st.map(rep_points[['latitude','longitude']])

    # Mostrar datos
    if st.checkbox('Mostrar datos'):
        st.write(rep_points)

    # Opción de descarga
    st.markdown(Helpers.get_table_download_link_csv(rep_points), unsafe_allow_html=True) 