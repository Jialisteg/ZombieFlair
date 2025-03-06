#!/usr/bin/env python3
"""
Punto de entrada para la Simulación de Sensores IoT con Zombis.
Ejecute este script para iniciar la aplicación.
"""

import sys
import os

# Añadir la raíz del proyecto a la ruta de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import ZombieSimulationCLI
from src import logger

if __name__ == "__main__":
    # Mostrar mensaje inicial
    logger.info("Iniciando aplicación de Simulación de Sensores IoT con Zombis")
    
    # Para activar el modo debug al inicio, descomente la siguiente línea:
    # logger.set_debug_mode(True)
    
    # Iniciar la aplicación
    app = ZombieSimulationCLI()
    app.run() 