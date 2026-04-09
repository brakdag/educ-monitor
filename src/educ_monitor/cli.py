import argparse
from datetime import datetime
from .scraper import get_llamados
from .database import init_db, add_llamado
from .notifier import connect_mqtt, publish_mqtt, disconnect_mqtt
from .config import config
from .logger import get_logger

logger = get_logger("cli")

def run_process() -> None:
    """
    Executes the main monitoring cycle.
    """
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    init_db()
    logger.info("Starting monitoring cycle...")
    llamados = get_llamados()
    
    allowed_schools = config.school_filter
    today = datetime.now().strftime("%Y-%m-%d")
    pending_notifications = []
    
    for llamado in llamados:
        unique_id = llamado['unique_id']
        tipo = llamado['tipo_llamado']
        fecha_llamado = llamado['fecha_llamado']
        fecha_publicacion = llamado['fecha_publicacion']
        
        is_new = add_llamado(
            unique_id, 
            str(llamado['raw_data']), 
            fecha_publicacion,
            tipo,
            fecha_llamado
        )
        
        if not is_new:
            continue
            
        is_allowed = not allowed_schools or llamado['escuela_id'] in allowed_schools
        if not is_allowed:
            continue
        
        if fecha_llamado and fecha_llamado < today:
            continue
                
        pending_notifications.append(llamado['raw_data'])
    
    if pending_notifications:
        client = connect_mqtt()
        for payload in pending_notifications:
            publish_mqtt(client, payload)
        if client:
            disconnect_mqtt(client)
        logger.info(f"Cycle complete. {len(pending_notifications)} notifications sent.")
    else:
        logger.info("Cycle complete. No new notifications to send.")

def main() -> None:
    """
    CLI Entry point for the Educ Monitor application.
    """
    parser = argparse.ArgumentParser(
        description="Educ Monitor - Monitoreo de llamados docentes",
        epilog="""Nota sobre el funcionamiento:
La aplicación registra SIEMPRE todos los llamados encontrados en 'llamados.db' para mantener un historial completo.
La notificación vóa MQTT solo se realiza si:
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

    if args.set_mqtt_ip:
        config.update_setting("MQTT_BROKER", args.set_mqtt_ip)
        logger.info(f"MQTT_BROKER updated to {args.set_mqtt_ip}")
    
    if args.set_mqtt_port:
        config.update_setting("MQTT_PORT", args.set_mqtt_port)
        logger.info(f"MQTT_PORT updated to {args.set_mqtt_port}")

    if args.set_topic:
        config.update_setting("MQTT_TOPIC", args.set_topic)
        logger.info(f"MQTT_TOPIC updated to {args.set_topic}")

    if args.set_filters:
        config.update_setting("SCHOOL_FILTER", args.set_filters)
        logger.info(f"SCHOOL_FILTER updated to {args.set_filters}")

    if args.show_config:
        print("Configuración actual:")
        print(f"MQTT_BROKER: {config.mqtt_broker}")
        print(f"MQTT_PORT: {config.mqtt_port}")
        print(f"MQTT_TOPIC: {config.mqtt_topic}")
        print(f"SCHOOL_FILTER: {config.school_filter}")

    if args.run:
        run_process()
    elif not any([args.set_mqtt_ip, args.set_mqtt_port, args.set_topic, args.set_filters, args.show_config]):
        parser.print_help()

if __name__ == "__main__":
    main()