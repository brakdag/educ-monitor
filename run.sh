#!/bin/bash
# Obtener la ruta del directorio donde se encuentra este script
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_ROOT"

# Cargar variables de entorno desde el archivo .env si existe
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Ejecutar el monitor
./venv/bin/python3 -m educ_monitor.cli --run >> cron.log 2>&1
