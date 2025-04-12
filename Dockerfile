
# Usa una imagen base de Airflow
FROM apache/airflow:2.10.5

# Copia los archivos de tu proyecto al contenedor
COPY requirements.txt /requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r /requirements.txt

# Copia los DAGs y otros archivos necesarios
COPY ./dags /opt/airflow/dags
COPY ./plugins /opt/airflow/plugins

# Expón el puerto (si es necesario)
EXPOSE 8080

