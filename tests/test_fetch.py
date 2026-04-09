import asyncio
import sys
from pathlib import Path

# Add src to path so we can import the module
sys.path.append(str(Path("src")))

from educ_monitor.scraper import get_llamados

async def main():
    print("Fetching data...")
    llamados = await get_llamados()
    print(f"Fetched {len(llamados)} items.")
    if llamados:
        print(llamados[0]) # Print first item to see structure

if __name__ == "__main__":
    asyncio.run(main())
