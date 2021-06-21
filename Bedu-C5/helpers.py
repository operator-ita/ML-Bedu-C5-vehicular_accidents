import base64
import pandas as pd

class Helpers():

    def get_table_download_link_csv(df):
        #csv = df.to_csv(index=False)
        csv = df.to_csv().encode()
        #b64 = base64.b64encode(csv.encode()).decode() 
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv" target="_blank">Descargar datos</a>'
        return href
