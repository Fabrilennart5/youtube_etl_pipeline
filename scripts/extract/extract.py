import os
import json
from pathlib import Path
from dotenv import load_dotenv
import googleapiclient.discovery
from datetime import datetime

# Configuración de paths
BASE_DIR = Path(__file__).parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_youtube_data():
    """Extrae y guarda datos del canal de YouTube"""
    load_dotenv()
    
    try:
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', 
            developerKey=os.getenv('YOUTUBE_API_KEY')
        )
        
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
        return filepath
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

# Bloque de ejecución directa
if __name__ == "__main__":
    print("🚀 Iniciando extracción de datos...")
    result = get_youtube_data()
    print("🎉 Extracción completada!")
