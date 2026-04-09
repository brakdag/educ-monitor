import sys
from pathlib import Path
import os

# Add src to path
sys.path.append(str(Path("src")))

from educ_monitor.scraper import get_llamados
from educ_monitor.config import config

def test_actual_scrape():
    # Force loading of current environment
    print(f"Filtering by schools: {config.SCHOOL_FILTER}")
    
    print("Fetching data...")
    llamados = get_llamados()
    print(f"Total fetched: {len(llamados)}")
    
    filtered = []
    if config.SCHOOL_FILTER:
        for l in llamados:
            if l['escuela_id'] in config.SCHOOL_FILTER:
                filtered.append(l)
    else:
        filtered = llamados
        
    print(f"Total after filter: {len(filtered)}")
    
    if filtered:
        print("\n--- Items matching filter ---")
        for i, item in enumerate(filtered[:5]): # Show up to 5
            print(f"{i+1}: {item['escuela_id']} - {item['tipo_llamado']} - {item['fecha_llamado']}")
    else:
        print("\nNo items found matching the filter.")

if __name__ == "__main__":
    test_actual_scrape()
