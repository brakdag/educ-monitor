#!/bin/bash
# install.sh - Configuración inicial de educ_monitor

echo "Iniciando instalación..."

# 1. Crear entorno virtual
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Entorno virtual creado."
fi
source venv/bin/activate

# 2. Instalar dependencias
echo "Instalando dependencias de Python..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Instalando navegadores para Playwright..."
playwright install chromium

# 3. Preparar configuración (.env)
if [ ! -f ".env" ]; then
    echo "Creando configuración inicial en .env..."
    cat <<EOF > .env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=educacionales/llamados
SCHOOL_FILTER=4117,4124,4114,4239,4063
EOF
fi

# 4. Asegurar permisos
chmod +x run.sh

# 5. Inicializar BD
echo "Inicializando base de datos..."
python3 -c "from db import init_db; init_db(); print('Base de datos creada exitosamente.')"

echo "Instalación completada con éxito."
