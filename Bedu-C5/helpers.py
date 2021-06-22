import base64
import pandas as pd
import pickle

class Helpers():

    def get_table_download_link_csv(df):
        #csv = df.to_csv(index=False)
        csv = df.to_csv().encode()
        #b64 = base64.b64encode(csv.encode()).decode() 
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv" target="_blank">Descargar datos</a>'
        return href

    def download_model(model):
        output_model = pickle.dumps(model)
        b64 = base64.b64encode(output_model).decode()
        href = f'<a href="data:file/output_model;base64,{b64}" download="model.pkl" target="_blank">Descargar modelo</a>'
        return href