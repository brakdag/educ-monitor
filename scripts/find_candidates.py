import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path("src")))

from educ_monitor.scraper import get_llamados

def find_vigente_schools():
    print("Fetching ALL data to find candidates...")
    llamados = get_llamados()
    today = datetime.now().strftime("%Y-%m-%d")
    
    candidates = {}
    
    for llamado in llamados:
        fecha = llamado['fecha_llamado']
        if fecha and fecha >= today:
            escuela_id = llamado['escuela_id']
            if escuela_id not in candidates:
                candidates[escuela_id] = []
            candidates[escuela_id].append(fecha)
    
    print(f"Found {len(candidates)} schools with active calls.")
    for esc_id, fechas in candidates.items():
        print(f"School {esc_id}: {len(fechas)} calls, earliest: {min(fechas)}")

if __name__ == "__main__":
    find_vigente_schools()
