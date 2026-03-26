import asyncio
import argparse
from datetime import datetime
from scraper import get_llamados
from db import init_db, add_llamado
from notifier import notify_home_assistant
from config import config

async def run_process():
    init_db()
    llamados = await get_llamados()
    
    allowed_schools = config.SCHOOL_FILTER
    today = datetime.now().strftime("%Y-%m-%d")
    
    for llamado in llamados:
        # Extract fields for database
        unique_id = llamado['unique_id']
        tipo = llamado['tipo_llamado']
        fecha_llamado = llamado['fecha_llamado']
        fecha_publicacion = llamado['fecha_publicacion']
        
        # 1. ALWAYS add to DB (record everything)
        # Using the raw_data for the content field in the DB for simplicity
        is_new = add_llamado(
            unique_id, 
            str(llamado['raw_data']), 
            fecha_publicacion,
            tipo,
            fecha_llamado
        )
        
        # 2. Filter for notification
        if not is_new:
            continue
            
        # School check
        is_allowed = not allowed_schools or llamado['escuela_id'] in allowed_schools
        if not is_allowed:
            continue
        
        # Date check

        if fecha_llamado and fecha_llamado < today:
            continue
                
        # It's new, allowed, and vigente!
        # Send raw_data for rich notification
        notify_home_assistant(llamado['raw_data'])
        print(f"Nuevo llamado vigente en Esc. {llamado['escuela_id']} enviado a MQTT.")

def main():
    parser = argparse.ArgumentParser(
        description="Educ Monitor - Monitoreo de llamados docentes",
        epilog="""Nota sobre el funcionamiento:
La aplicación registra SIEMPRE todos los llamados encontrados en 'llamados.db' para mantener un historial completo.
La notificación vía MQTT solo se realiza si:
1. El llamado es nuevo (no registrado previamente).
2. La escuela está dentro de los filtros configurados (si existen).
3. La fecha del llamado es igual o posterior a la fecha actual (vigente).
"""
    )
    parser.add_argument("--run", action="store_true", help="Ejecutar el ciclo de monitoreo")
    parser.add_argument("--set-mqtt-ip", help="Configurar IP del broker MQTT")
    parser.add_argument("--set-mqtt-port", type=int, help="Configurar puerto del broker MQTT")
    parser.add_argument("--set-topic", help="Configurar tópico MQTT")
    parser.add_argument("--set-filters", help="Configurar filtros de escuelas (ej: 4117,4124)")
    parser.add_argument("--show-config", action="store_true", help="Mostrar configuración actual")

    args = parser.parse_args()

    # Apply configuration updates
    if args.set_mqtt_ip:
        config.update_setting("MQTT_BROKER", args.set_mqtt_ip)
        print(f"MQTT_BROKER actualizado a {args.set_mqtt_ip}")
    
    if args.set_mqtt_port:
        config.update_setting("MQTT_PORT", args.set_mqtt_port)
        print(f"MQTT_PORT actualizado a {args.set_mqtt_port}")

    if args.set_topic:
        config.update_setting("MQTT_TOPIC", args.set_topic)
        print(f"MQTT_TOPIC actualizado a {args.set_topic}")

    if args.set_filters:
        config.update_setting("SCHOOL_FILTER", args.set_filters)
        print(f"SCHOOL_FILTER actualizado a {args.set_filters}")

    # Show config
    if args.show_config:
        print("Configuración actual:")
        print(f"MQTT_BROKER: {config.MQTT_BROKER}")
        print(f"MQTT_PORT: {config.MQTT_PORT}")
        print(f"MQTT_TOPIC: {config.MQTT_TOPIC}")
        print(f"SCHOOL_FILTER: {config.SCHOOL_FILTER}")

    # Run execution
    if args.run:
        asyncio.run(run_process())
    elif not any([args.set_mqtt_ip, args.set_mqtt_port, args.set_topic, args.set_filters, args.show_config]):
        parser.print_help()

if __name__ == "__main__":
    main()
