FROM python:3.8

# Definir directorio de trabajo
WORKDIR /Bedu-C5

# Copiar e instalar dependencias al nuevo directorio
COPY requirement.txt .
RUN pip install -r requirement.txt 

# Copiar la carpeta de trabajo al servidor
COPY ./Bedu-C5 ./Bedu-C5

# Exponer puerto
EXPOSE 8501

#Crear imagen  
CMD ["streamlit", "run", "./Bedu-C5/app.py"]