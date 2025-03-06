#!/usr/bin/env python3
"""
Módulo de registro (logger) para la Simulación de Sensores IoT con Zombis.
Proporciona funcionalidades de registro y depuración.
"""

import os
import logging
import datetime
from pathlib import Path

# Crear directorio de logs si no existe
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = logs_dir / f"zombies_simulation_{current_time}.log"

# Configurar el logger
logger = logging.getLogger("zombie_simulation")
logger.setLevel(logging.INFO)  # Nivel por defecto

# Manejador de archivo para todos los mensajes
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # El archivo captura todo

# Manejador de consola solo para errores en producción
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)  # Por defecto solo muestra errores

# Formato de los mensajes de log
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Añadir los manejadores al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Variable global para control del modo debug
DEBUG_MODE = False

def set_debug_mode(enabled=True):
    """
    Activa o desactiva el modo DEBUG.
    
    Args:
        enabled (bool): True para activar, False para desactivar
    """
    global DEBUG_MODE
    DEBUG_MODE = enabled
    
    # Configurar el nivel de log apropiado
    if DEBUG_MODE:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        logger.debug("Modo DEBUG activado")
    else:
        logger.setLevel(logging.INFO)
        console_handler.setLevel(logging.ERROR)
        logger.info("Modo DEBUG desactivado")

def debug(message):
    """
    Registra un mensaje de nivel DEBUG.
    
    Args:
        message (str): El mensaje a registrar
    """
    logger.debug(message)

def info(message):
    """
    Registra un mensaje de nivel INFO.
    
    Args:
        message (str): El mensaje a registrar
    """
    logger.info(message)

def warning(message):
    """
    Registra un mensaje de nivel WARNING.
    
    Args:
        message (str): El mensaje a registrar
    """
    logger.warning(message)

def error(message):
    """
    Registra un mensaje de nivel ERROR.
    
    Args:
        message (str): El mensaje a registrar
    """
    logger.error(message)

def critical(message):
    """
    Registra un mensaje de nivel CRITICAL.
    
    Args:
        message (str): El mensaje a registrar
    """
    logger.critical(message)

def is_debug_enabled():
    """
    Verifica si el modo DEBUG está activado.
    
    Returns:
        bool: True si el modo DEBUG está activado, False en caso contrario
    """
    return DEBUG_MODE

# Registro inicial de la aplicación
info("Aplicación de Simulación de Sensores IoT con Zombis iniciada") 