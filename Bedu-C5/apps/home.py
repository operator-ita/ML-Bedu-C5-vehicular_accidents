import streamlit as st
import pandas as pd 
import numpy as np
import os 
def app():
    
    st.title('El problema vehicular en la CDMX')

    st.write('En ésta página se explica el problema y nuestras hipótesis.')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    st.write(dir_path)
    
    df = pd.read_csv(
        "/Bedu-C5/Bedu-C5/apps/data/most_dangerous_geop.csv", sep=",", index_col=0)

    st.map(df[['latitude','longitude']])