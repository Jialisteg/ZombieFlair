# Simulación de Sensores IoT con Zombis

Una aplicación CLI en Python que simula un edificio infestado de zombis, utilizando sensores IoT para rastrear la invasión.

## Descripción

Esta aplicación simula un escenario donde un edificio está infestado de zombis, y se utilizan sensores IoT para detectar su presencia. El usuario puede configurar el edificio, añadir zombis iniciales y simular la propagación de la infestación turno por turno.

## Características

- Configurar un edificio con múltiples pisos y habitaciones
- Añadir zombis iniciales a habitaciones aleatorias
- Simular el movimiento de zombis entre habitaciones adyacentes
- Rastrear el estado de cada habitación y sensor
- Limpiar habitaciones de zombis
- Restablecer sensores que han sido activados
- **Modo DEBUG** para diagnosticar problemas y ver información detallada
- **Sistema de Logs** que registra todas las acciones de la aplicación

## Instalación

1. Clonar este repositorio:
   ```
   git clone https://github.com/yourusername/zombie-iot-simulation.git
   cd zombie-iot-simulation
   ```

2. No se requieren dependencias adicionales ya que la aplicación utiliza solo bibliotecas estándar de Python.

## Uso

1. Ejecutar la aplicación:
   ```
   python run.py
   ```

2. Seguir el menú en pantalla para interactuar con la simulación:
   - Opción 1: Configurar Edificio - Configurar el número de pisos y habitaciones
   - Opción 2: Mostrar Estado del Edificio - Mostrar el estado actual del edificio
   - Opción 3: Avanzar Simulación - Mover zombis a habitaciones adyacentes
   - Opción 4: Limpiar Habitación - Eliminar zombis de una habitación específica
   - Opción 5: Restablecer Sensor - Restablecer un sensor al estado normal
   - Opción 6: Activar/Desactivar modo DEBUG - Cambiar el nivel de detalle de los logs
   - Opción 7: Mostrar información de depuración - Ver detalles internos (solo en modo DEBUG)
   - Opción 8: Salir - Salir de la aplicación

## Arquitectura

La aplicación está estructurada utilizando principios de programación orientada a objetos:

- **Edificio (Building)**: Administra una colección de pisos y proporciona métodos para acceder a las habitaciones
- **Piso (Floor)**: Contiene múltiples habitaciones y maneja las conexiones entre ellas
- **Habitación (Room)**: Representa un espacio físico que puede contener zombis y tiene un sensor
- **Sensor**: Detecta la presencia de zombis y puede estar en estado "normal" o "alerta"
- **Simulación (Simulation)**: Orquesta la lógica de movimiento de zombis y rastrea el estado del juego
- **ZombieSimulationCLI**: Proporciona la interfaz de línea de comandos para la interacción del usuario

## Estructura del Proyecto

La organización de archivos y carpetas del proyecto es la siguiente:

```
├── README.md             # Documentación del proyecto
├── run.py                # Punto de entrada para ejecutar la aplicación
├── .gitignore            # Archivos y carpetas ignorados por git
├── logs/                 # Directorio donde se almacenan los archivos de log
├── src/                  # Código fuente principal
│   ├── main.py           # CLI principal para interacción del usuario
│   ├── simulation.py     # Lógica de simulación de zombis
│   ├── logger.py         # Módulo de registro y depuración
│   └── models/           # Modelos de datos para la aplicación
│       ├── __init__.py   # Inicializador del paquete models
│       ├── building.py   # Clase Edificio
│       ├── floor.py      # Clase Piso
│       ├── room.py       # Clase Habitación 
│       └── sensor.py     # Clase Sensor
```

### Lógica de Movimiento de Zombis

- Los zombis se propagan a habitaciones adyacentes en cada turno
- Las habitaciones se consideran adyacentes si tienen números de habitación consecutivos en el mismo piso
- Las habitaciones también están conectadas verticalmente entre pisos (mismo número de habitación en diferentes pisos)
- Cuando los zombis entran en una habitación, el sensor entra en estado de alerta
- La simulación termina cuando todas las habitaciones están infestadas

## Modo DEBUG y Logging

La aplicación cuenta con un sistema de registro que guarda todas las acciones en archivos de log dentro del directorio `logs/`. El nombre del archivo incluye la fecha y hora de ejecución para facilitar el seguimiento.

### Niveles de log

- **DEBUG**: Información detallada para diagnóstico de problemas
- **INFO**: Información general sobre la ejecución normal
- **WARNING**: Advertencias sobre problemas potenciales
- **ERROR**: Errores que permiten continuar la ejecución
- **CRITICAL**: Errores graves que impiden continuar

### Activar modo DEBUG

Para activar el modo DEBUG durante la ejecución, seleccione la opción 6 del menú principal. Cuando el modo DEBUG está activado:

1. Se muestra un indicador en el encabezado de la aplicación
2. Los mensajes de depuración se muestran en la consola
3. Se habilita una opción adicional (7) que muestra información detallada de depuración

Todos los mensajes, independientemente del nivel, siempre se guardan en el archivo de log para referencia futura.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 