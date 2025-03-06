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

if __name__ == "__main__":
    app = ZombieSimulationCLI()
    app.run() 