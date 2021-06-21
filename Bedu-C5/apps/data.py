import streamlit as st
import numpy as np
import pandas as pd
from helpers import Helpers

def app():
    st.title('Datos')

    st.write("Los siguientes son los datos obtenidos del `C5` de la CDMX.")

    df = pd.read_csv("/Bedu-C5/Bedu-C5/apps/data/incidentes-viales-c5-limpio.csv", sep="$", index_col=0)
    
    st.write(df.head())


