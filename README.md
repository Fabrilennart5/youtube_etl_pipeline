# YouTube ETL Pipeline 🚀

![Imagen para el proyecto](https://pbs.twimg.com/media/GoXR7xuWsAA5q0U?format=jpg&name=900x900)

**Pipeline ETL automatizado para extracción de datos de YouTube** que utiliza Apache Airflow y Docker. Diseñado para obtener estadísticas de canales/videos, procesarlas y almacenarlas en SQLite.

---

## 📌 Requisitos

Para ejecutar este proyecto, asegúrate de tener lo siguiente:

1. **API Key de YouTube**: Obtén una API Key válida desde Google Cloud Platform para acceder a la API de YouTube.
2. **ID del canal de YouTube**: Identifica el canal del cual deseas extraer datos. (Ej: `UC_x5XG1OV2P6uZZ5FSM9Ttw`)
3. **Docker**: Necesitas Docker y Docker Compose instalados en tu sistema.
4. **uv**: Para la gestión de dependencias en un entorno local.

---

## 🛠️ Instalación

Sigue estos pasos para instalar y configurar el proyecto:

Sigue estos pasos para instalar y configurar el proyecto:

1. **Clona el repositorio**:
   ```bash
   git clone git@github.com:Fabrilennart5/youtube_etl_pipeline.git
   cd youtube_etl_pipeline


2. **Configura la API Key y el ID del canal**:
    
    ```bash
    echo "API_KEY=tu_api_key_aqui" > .env
    echo "CHANNEL_ID=id_del_canal" >> .env
    ```
    
3. **Configura Docker (opcional)**:
    
    ```bash
    docker-compose build
    ```
    
4. **Levanta el entorno Docker**:
    
    ```bash
    docker-compose up -d
    ```
    
5. **Instalación local con uv**:
    
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

## 🚀 Ejecución

### Con Docker:

1. Accede a la interfaz de Airflow en `http://localhost:8080`
    
2. Activa el DAG `youtube_etl_dag`
    
3. Verifica los datos en `data/processed/`
    

### Localmente:

```bash
python dags/youtube_etl_dag.py
```

### Estructura de salida:

```bash
data/
├── raw/              # JSON crudos
├── processed/        # CSV transformados
└── data_base/        # SQLite con datos finales
```

---

## ⚙️ Configuración Adicional

- **Variables de entorno**: Configura `API_KEY` y `CHANNEL_ID` en `.env`
    
- **Puertos**: Verifica disponibilidad de puertos (8080 para Airflow)
    
- **Logs**: Revisa los logs en `logs/` para diagnóstico de errores
    

---

## 🔄 Flujo del Pipeline

1. **Extracción**: Obtiene estadísticas del canal mediante YouTube API
    
2. **Transformación**: Convierte JSON a CSV estructurado
    
3. **Carga**: Almacena en SQLite con metadatos de ejecución
    

---

## ▶️ Tutorial de Funcionamiento

**Video explicativo del proyecto**:  
[![DuckDB + ETL con Python](https://img.shields.io/badge/Ver_Tutorial-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.linkedin.com/posts/fabricio-lennart_duckdb-etl-python-activity-7316911074480447488-9C76?utm_source=share&utm_medium=member_desktop&rcm=ACoAACJ0kvIB-RfjThNzVfvOPXGuLylc2ySNWLY)



