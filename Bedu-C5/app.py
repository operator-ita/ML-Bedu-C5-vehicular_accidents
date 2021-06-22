import streamlit as st
from multiapp import MultiApp
from apps import home, dbscan, data, kmeans # import your app modules here
from helpers import Helpers

app = MultiApp()

st.markdown("""
# Bedu-C5-vehicular_accidents

En ésta página se encuentra el proyecto de análisis de accidentes vehiculares en la CDMX del 2017-2021. Documentación completa en [github](https://github.com/operator-ita/Bedu-C5-vehicular_accidents.git) elaborado por [Lara Elías](https://github.com/operator-ita), [Luis Jimenez](https://github.com/Luisjimherz) y [Mario Cantú](https://github.com/Mario-16180). Proyecto final para [BEDU](https://bedu.org/).
""")

# Add all your application here
app.add_app("Inicio", home.app)
app.add_app("Datos", data.app)
app.add_app("Clusterización", dbscan.app)
app.add_app("Centros de atención", kmeans.app)
# The main app
app.run()