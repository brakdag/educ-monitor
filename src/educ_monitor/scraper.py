import requests
import time
from datetime import datetime
from .config import config

def get_llamados():
    session = requests.Session()
    
    # Headers configuration from config object
    headers = config.DEFAULT_HEADERS.copy()
    headers["User-Agent"] = config.USER_AGENT

    try:
        # 1. Establish session
        session.get("https://educacionales.mendoza.edu.ar/", headers={"User-Agent": config.USER_AGENT})
        
        # 2. Fetch data
        timestamp = int(time.time() * 1000)
        url = f"https://educacionales.mendoza.edu.ar/data?_={timestamp}"
        
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        llamados = []
        if "datos" in data:
            for item in data["datos"]:
                unique_id = str(item.get("id"))
                
                escuela_info = item.get("lugar_trabajo", "")
                escuela_id = escuela_info.split(' - ')[0] if ' - ' in escuela_info else escuela_info
                
                fecha_raw = item.get("fecha_llamado_1")
                fecha_llamado = None
                if fecha_raw:
                    try:
                        fecha_llamado = datetime.strptime(fecha_raw.split(' ')[0], "%d/%m/%y").strftime("%Y-%m-%d")
                    except:
                        pass
                
                llamado_data = {
                    "unique_id": unique_id,
                    "escuela_id": escuela_id,
                    "tipo_llamado": item.get("tipo_llamado", ""),
                    "fecha_llamado": fecha_llamado,
                    "fecha_publicacion": datetime.now().strftime("%Y-%m-%d"),
                    "raw_data": item
                }
                
                llamados.append(llamado_data)
        
        return llamados
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []