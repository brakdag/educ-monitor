import sys
from pathlib import Path
from datetime import datetime

# Añadir src al path
sys.path.append(str(Path("src")))

from educ_monitor.scraper import get_llamados
from educ_monitor.notifier import connect_mqtt, publish_mqtt, disconnect_mqtt
from educ_monitor.config import config

def run_integration_test():
    print(f"--- Iniciando prueba de integración MQTT ---")
    print(f"Broker: {config.MQTT_BROKER}:{config.MQTT_PORT}")
    print(f"Tópico: {config.MQTT_TOPIC}")
    print(f"Filtros: {config.SCHOOL_FILTER}")
    
    # 1. Obtener llamados
    print("Obteniendo datos...")
    llamados = get_llamados()
    
    # 2. Filtrar
    allowed_schools = config.SCHOOL_FILTER
    today = datetime.now().strftime("%Y-%m-%d")
    
    found_any = False
    
    # 3. Conectar al MQTT
    print("Conectando al broker MQTT...")
    try:
        client = connect_mqtt()
        
        for llamado in llamados:
            # Filtrar por escuela
            if allowed_schools and llamado['escuela_id'] not in allowed_schools:
                continue
                
            # Filtrar por vigencia
            fecha_llamado = llamado['fecha_llamado']
            if fecha_llamado and fecha_llamado < today:
                continue
            
            print(f"Encontrado llamado vigente: {llamado['escuela_id']} - {llamado['tipo_llamado']}")
            
            # Enviar
            publish_mqtt(client, llamado['raw_data'])
            print("¡Notificación enviada correctamente!")
            found_any = True
        
        # Desconectar
        disconnect_mqtt(client)
    except Exception as e:
        print(f"Error durante el proceso MQTT: {e}")
            
    if not found_any:
        print("No se encontraron llamados vigentes para las escuelas filtradas.")

if __name__ == "__main__":
    run_integration_test()
