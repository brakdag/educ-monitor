# Roles de Automatización (Agentes)

## 1. Agente Scraper (Eficiente, c/1 hora)
- **Objetivo:** Obtener datos dinámicos con consumo optimizado.
- **Acción:**
    1. Ejecuta Playwright en modo headless, bloqueando recursos innecesarios.
    2. Intercepta la petición de red a `/data` para capturar el JSON directamente.

## 2. Agente Analista
- **Objetivo:** Comparación de estados.
- **Acción:** Compara los datos recién obtenidos con el último registro en la base de datos SQLite. Identifica únicamente las filas nuevas.

## 3. Agente Notificador (Integración MQTT)
- **Objetivo:** Integración y envío de datos.
- **Acción:** 
    1. Se conecta al Broker MQTT local.
    2. Publica un mensaje JSON con los detalles del nuevo llamado en el topic configurado.
    3. **Automatización:** Home Assistant (o cualquier cliente MQTT) recibe el mensaje y dispara las acciones deseadas.
