from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import json
import duckdb
import sqlite3
import csv
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path="/opt/airflow/.env")

# Paths base
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "data" / "data_base" / "youtube.db"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
(DB_PATH.parent).mkdir(parents=True, exist_ok=True)

def extract_youtube_data():
    """Extrae y guarda datos del canal de YouTube"""
    load_dotenv()
    try:
        from googleapiclient.discovery import build

        youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
        response = youtube.channels().list(
            part='snippet,statistics',
            id=os.getenv('YOUTUBE_CHANNEL_ID')
        ).execute()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"channel_data_{timestamp}.json"
        filepath = RAW_DATA_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)

        print(f"✅ Datos guardados en: {filepath}")
        print(f"📊 Estadísticas: {response['items'][0]['statistics']}")
    except Exception as e:
        print(f"❌ Error en extracción: {str(e)}")
        raise

def transform_data():
    """Transforma los datos crudos y guarda un CSV procesado"""
    try:
        raw_files = list(RAW_DATA_DIR.glob("channel_data_*.json"))
        if not raw_files:
            raise FileNotFoundError("No se encontraron archivos JSON")

        latest_file = max(raw_files, key=lambda f: f.stat().st_mtime)

        conn = duckdb.connect(database=':memory:')
        conn.execute("""
        CREATE TEMP TABLE channel_stats AS
        SELECT 
            items[1].id AS channel_id,
            items[1].snippet.title AS channel_name,
            items[1].statistics.viewCount AS views,
            items[1].statistics.subscriberCount AS subscribers,
            items[1].statistics.videoCount AS videos,
            CURRENT_TIMESTAMP AS processed_at
        FROM read_json_auto(?)
        """, [str(latest_file)])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = PROCESSED_DIR / f"channel_stats_{timestamp}.csv"

        conn.execute(f"""
        COPY channel_stats TO '{output_csv}' (HEADER, DELIMITER ',')
        """)

        print(f"✅ Datos transformados guardados en: {output_csv}")
    except Exception as e:
        print(f"❌ Error en transformación: {str(e)}")
        raise

def load_data():
    """Carga el CSV procesado a SQLite"""
    try:
        csv_files = list(PROCESSED_DIR.glob("channel_stats_*.csv"))
        if not csv_files:
            raise FileNotFoundError("No se encontraron archivos CSV")

        latest_csv = max(csv_files, key=lambda f: f.stat().st_mtime)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS channel_stats (
            channel_id TEXT PRIMARY KEY,
            channel_name TEXT,
            views INTEGER,
            subscribers INTEGER,
            videos INTEGER,
            processed_at TIMESTAMP,
            load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        with open(latest_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                INSERT OR REPLACE INTO channel_stats 
                (channel_id, channel_name, views, subscribers, videos, processed_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    row['channel_id'],
                    row['channel_name'],
                    int(row['views']),
                    int(row['subscribers']),
                    int(row['videos']),
                    row['processed_at']
                ))

        conn.commit()
        print(f"✅ Datos cargados en SQLite: {DB_PATH}")
        print(f"📊 Total registros: {cursor.execute('SELECT COUNT(*) FROM channel_stats').fetchone()[0]}")
    except Exception as e:
        print(f"❌ Error en carga: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

# Definición del DAG
default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    dag_id='youtube_etl_dag',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False,
    description='ETL para estadísticas de YouTube'
) as dag:

    t1 = PythonOperator(
        task_id='extract_data',
        python_callable=extract_youtube_data
    )

    t2 = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    t3 = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    t1 >> t2 >> t3

