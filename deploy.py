#!/usr/bin/env python3
"""
Script de despliegue para la Simulación de Sensores IoT con Zombis.
Este script automatiza la configuración del entorno y la instalación de la aplicación.
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path


def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Se requiere Python {required_version[0]}.{required_version[1]} o superior.")
        print(f"Versión actual: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        sys.exit(1)
    
    print(f"✓ Versión de Python compatible: {current_version[0]}.{current_version[1]}.{current_version[2]}")


def create_virtual_environment(venv_path, force=False):
    """Crea un entorno virtual de Python."""
    if os.path.exists(venv_path):
        if force:
            print(f"! Eliminando entorno virtual existente en: {venv_path}")
            shutil.rmtree(venv_path)
        else:
            print(f"✓ Entorno virtual ya existe en: {venv_path}")
            return
    
    print(f"Creando entorno virtual en: {venv_path}")
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    print("✓ Entorno virtual creado correctamente.")


def install_requirements(venv_path):
    """Instala los requisitos en el entorno virtual."""
    if sys.platform == 'win32':
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    print("Actualizando pip...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    
    print("Instalando requisitos...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    
    print("✓ Requisitos instalados correctamente.")


def install_package(venv_path, dev_mode=False):
    """Instala el paquete en el entorno virtual."""
    if sys.platform == 'win32':
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    if dev_mode:
        print("Instalando paquete en modo desarrollo...")
        subprocess.run([pip_path, "install", "-e", "."], check=True)
    else:
        print("Instalando paquete...")
        subprocess.run([pip_path, "install", "."], check=True)
    
    print("✓ Paquete instalado correctamente.")


def create_logs_directory():
    """Crea el directorio de logs si no existe."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("✓ Directorio de logs creado.")
    else:
        print("✓ Directorio de logs ya existe.")


def create_launcher(venv_path):
    """Crea scripts de lanzamiento para diferentes plataformas."""
    if sys.platform == 'win32':
        # Crear batch script para Windows
        with open("ejecutar_simulacion.bat", "w") as f:
            f.write(f'@echo off\n')
            f.write(f'echo Iniciando Simulacion de Sensores IoT con Zombis...\n')
            f.write(f'call {os.path.join(venv_path, "Scripts", "activate.bat")}\n')
            f.write(f'python run.py\n')
            f.write(f'pause\n')
        print("✓ Creado launcher para Windows: ejecutar_simulacion.bat")
    else:
        # Crear shell script para Unix/Linux/Mac
        launcher_path = "ejecutar_simulacion.sh"
        with open(launcher_path, "w") as f:
            f.write(f'#!/bin/bash\n')
            f.write(f'echo "Iniciando Simulacion de Sensores IoT con Zombis..."\n')
            f.write(f'source {os.path.join(venv_path, "bin", "activate")}\n')
            f.write(f'python run.py\n')
        
        # Hacer ejecutable el script
        os.chmod(launcher_path, 0o755)
        print(f"✓ Creado launcher para Unix: {launcher_path}")


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Script de despliegue para la Simulación de Sensores IoT con Zombis")
    parser.add_argument("--venv", default=".venv", help="Ruta del entorno virtual (predeterminado: .venv)")
    parser.add_argument("--force", action="store_true", help="Forzar recreación del entorno virtual")
    parser.add_argument("--dev", action="store_true", help="Instalar en modo desarrollo")
    args = parser.parse_args()
    
    print("=" * 80)
    print("DESPLIEGUE DE SIMULACIÓN DE SENSORES IOT CON ZOMBIS")
    print("=" * 80)
    
    try:
        # Verificar versión de Python
        check_python_version()
        
        # Crear entorno virtual
        create_virtual_environment(args.venv, args.force)
        
        # Instalar requisitos
        install_requirements(args.venv)
        
        # Instalar paquete
        install_package(args.venv, args.dev)
        
        # Crear directorio de logs
        create_logs_directory()
        
        # Crear launcher
        create_launcher(args.venv)
        
        print("\n" + "=" * 80)
        print("¡DESPLIEGUE COMPLETADO EXITOSAMENTE!")
        print(f"Para ejecutar la aplicación, use: {'ejecutar_simulacion.bat' if sys.platform == 'win32' else './ejecutar_simulacion.sh'}")
        print("=" * 80)
        
    except subprocess.CalledProcessError as e:
        print(f"\nError durante el despliegue: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 