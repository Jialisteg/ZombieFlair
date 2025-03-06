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
- Uso del arma secreta para eliminar zombis aleatoriamente
- Agregar zombis manualmente durante la simulación
- Activar/desactivar la generación automática de zombis
- Visualización mejorada del edificio con formato compacto
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

   ### Menú Principal
   - Opción 0: Instrucciones del Juego - Muestra información sobre cómo jugar
   - Opción 1: Configurar Edificio - Configurar el número de pisos y habitaciones
   - Opción 2: Comenzar Simulación - Inicia la simulación interactiva
   - Opción 3: Activar/Desactivar modo DEBUG - Cambiar el nivel de detalle de los logs
   - Opción 4: Mostrar información de depuración - Ver detalles internos (solo en modo DEBUG)
   - Opción 5: Salir - Salir de la aplicación

   ### Menú de Juego (Durante la Simulación)
   - Opción 1: Avanzar otro turno - Avanza la simulación un turno (funciona con Enter)
   - Opción 2: Agregar otro Zombie - Añade un zombi en una habitación aleatoria
   - Opción 3: Limpiar Habitación - Elimina zombis de una habitación específica
   - Opción 4: Restablecer Sensor - Restablece un sensor al estado normal
   - Opción 5: Activar/Desactivar Generación de Zombis - Controla la generación automática
   - Opción 6: Utilizar el arma secreta - Elimina zombis aleatoriamente (50% de probabilidad)
   - Opción 7: Agregar Practicante - Funcionalidad en desarrollo
   - Opción 8: Volver al menú principal - Regresa al menú principal

## Arquitectura

La aplicación está estructurada utilizando principios de programación orientada a objetos:

- **Edificio (Building)**: Administra una colección de pisos y proporciona métodos para acceder a las habitaciones
- **Piso (Floor)**: Contiene múltiples habitaciones y maneja las conexiones entre ellas
- **Habitación (Room)**: Representa un espacio físico que puede contener zombis y tiene un sensor
- **Escalera (Staircase)**: Un tipo especial de habitación que permite el movimiento vertical entre pisos
- **Sensor**: Detecta la presencia de zombis y puede estar en estado "normal" o "alerta"
- **Practicante**: Representa al interno que se mueve por el edificio y debe ser protegido de los zombis
- **Simulación (Simulation)**: Orquesta la lógica de movimiento de zombis y rastrea el estado del juego
- **ZombieSimulationCLI**: Proporciona la interfaz de línea de comandos para la interacción del usuario

## Estructura del Proyecto

La organización de archivos y carpetas del proyecto es la siguiente:

```
├── README.md             # Documentación del proyecto
├── README_TESTS.md       # Documentación específica para tests
├── run.py                # Punto de entrada para ejecutar la aplicación
├── .gitignore            # Archivos y carpetas ignorados por git
├── logs/                 # Directorio donde se almacenan los archivos de log
├── src/                  # Código fuente principal
│   ├── main.py           # CLI principal para interacción del usuario
│   ├── simulation.py     # Lógica de simulación de zombis
│   ├── logger.py         # Módulo de registro y depuración
│   ├── fix.md            # Documentación sobre las correcciones de interfaz
│   └── models/           # Modelos de datos para la aplicación
│       ├── __init__.py   # Inicializador del paquete models
│       ├── building.py   # Clase Edificio
│       ├── floor.py      # Clase Piso
│       ├── room.py       # Clase Habitación 
│       ├── staircase.py  # Clase Escalera
│       ├── sensor.py     # Clase Sensor
│       └── practicante.py # Clase Practicante
├── tests/                # Pruebas unitarias
│   ├── __init__.py       # Inicializador del paquete tests
│   ├── conftest.py       # Configuración y fixtures para tests
│   ├── test_models.py    # Tests para modelos (Building, Floor, Room, etc.)
│   └── test_simulation.py # Tests para la lógica de simulación
```

### Visualización del Edificio

La visualización del edificio se muestra en un formato claro y compacto:

```
Piso 1:
  Esc 0           Hab 1          Hab 2          Hab 3
  [🧟 🪜 🟢   ]     [   🚪 🟢   ]     [   🚪 🟢   ]     [   🚪 🟢   ]

Piso 0:
  Esc 0           Hab 1          Hab 2          Hab 3
  [   🪜      ]     [   🚪 🟢 🚶]     [🧟 🚪 🚨   ]     [   🚪 🟢   ]
```

Donde:
- `Esc`: Escalera - permite movimiento vertical entre pisos
- `Hab`: Habitación regular
- `🧟`: Presencia de zombi
- `🪜`: Escalera
- `🚪`: Puerta (habitación regular)
- `🚨`: Sensor en estado de alerta
- `🟢`: Sensor en estado normal
- `🚶`: Practicante (debe ser protegido de los zombies)

### Lógica de Movimiento de Zombis

- Los zombis se propagan a habitaciones adyacentes en cada turno
- **Movimiento Horizontal**: Las habitaciones se consideran adyacentes si tienen números de habitación consecutivos en el mismo piso
- **Movimiento Vertical**: Los zombis pueden moverse entre pisos ÚNICAMENTE a través de las escaleras (habitación 0 de cada piso)
- Las escaleras permiten a los zombis moverse hacia el piso superior o inferior
- Las escaleras NO tienen sensores, pero permiten la propagación vertical de zombis
- Cuando los zombis entran en una habitación normal, el sensor entra en estado de alerta
- La simulación termina cuando todas las habitaciones están infestadas o un zombi captura al practicante

### Funcionalidades Adicionales

1. **Arma Secreta**:
   - Permite eliminar zombis de varias habitaciones a la vez
   - Cada zombi tiene 50% de probabilidad de ser eliminado
   - Los sensores permanecen en alerta incluso si los zombis son eliminados

2. **Practicante (Interno)**:
   - Simbolizado por el icono 🚶
   - Solo puede haber un practicante a la vez en el edificio
   - Se mueve automáticamente en cada turno a habitaciones adyacentes sin zombis
   - No activa los sensores al entrar en una habitación
   - Si un zombi llega a la misma habitación que el practicante, el juego termina
   - Añade un elemento de estrategia, ya que debes mantenerlo protegido de los zombis

3. **Entrada Validada**:
   - Durante la configuración, se validan todas las entradas
   - Se puede escribir 'salir' en cualquier momento para volver al menú principal
   - La aplicación solicita nuevos datos si los valores ingresados no son válidos

4. **Redirección Automática**:
   - Si se intenta comenzar la simulación sin un edificio configurado, la aplicación redirige automáticamente a la configuración del edificio

## Modo DEBUG y Logging

La aplicación cuenta con un sistema de registro que guarda todas las acciones en archivos de log dentro del directorio `logs/`. El nombre del archivo incluye la fecha y hora de ejecución para facilitar el seguimiento.

### Niveles de log

- **DEBUG**: Información detallada para diagnóstico de problemas
- **INFO**: Información general sobre la ejecución normal
- **WARNING**: Advertencias sobre problemas potenciales
- **ERROR**: Errores que permiten continuar la ejecución
- **CRITICAL**: Errores graves que impiden continuar

### Activar modo DEBUG

Para activar el modo DEBUG durante la ejecución, seleccione la opción 3 del menú principal. Cuando el modo DEBUG está activado:

1. Se muestra un indicador en el encabezado de la aplicación
2. Los mensajes de depuración se muestran en la consola
3. Se habilita una opción adicional (4) que muestra información detallada de depuración

Todos los mensajes, independientemente del nivel, siempre se guardan en el archivo de log para referencia futura.

## Despliegue y Ejecución

El proyecto ofrece múltiples formas de despliegue para adaptarse a diferentes entornos y necesidades.

### 1. Script de Despliegue Automático

Para una instalación rápida y sencilla, utilice el script de despliegue:

```bash
# Instalación básica
python deploy.py

# Instalación con entorno virtual personalizado
python deploy.py --venv entorno_personalizado

# Instalación forzada (recrear entorno virtual)
python deploy.py --force

# Instalación en modo desarrollo
python deploy.py --dev
```

El script realizará las siguientes acciones:
- Verificar la versión de Python
- Crear un entorno virtual
- Instalar dependencias
- Configurar el proyecto
- Crear scripts de lanzamiento específicos para cada plataforma

Una vez completado, podrá ejecutar la aplicación con:
- Windows: `ejecutar_simulacion.bat`
- Linux/Mac: `./ejecutar_simulacion.sh`

### 2. Instalación como Paquete Python

También puede instalar el proyecto como un paquete Python:

```bash
# Crear y activar entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
.venv\Scripts\activate     # En Windows

# Instalar el paquete
pip install -e .

# Ejecutar la aplicación
zombie-sim
```

### 3. Despliegue con Docker

Para un despliegue aislado y consistente, utilice Docker:

```bash
# Construir y ejecutar con Docker Compose
docker-compose up

# O construir y ejecutar manualmente
docker build -t zombies-iot-simulation .
docker run -it --name zombies-iot -v ./logs:/app/logs zombies-iot-simulation
```

### 4. Configuración

La aplicación utiliza un archivo de configuración `config.yaml` que permite personalizar diversos aspectos:

- Valores predeterminados para la configuración del edificio
- Probabilidades para eventos aleatorios
- Configuración del sistema de logs
- Parámetros de la interfaz

Puede editar este archivo para ajustar el comportamiento de la aplicación según sus preferencias.

## New Feature: Interactive Web Visualization

In addition to the CLI interface, this project now includes a modern web-based visualization built with FastAPI and React.

### Backend API (FastAPI)

The FastAPI backend provides a RESTful API for interacting with the simulation:

#### Running the API Server

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start the FastAPI server:
   ```
   python run_api.py
   ```

3. The API will be available at http://localhost:5000
   - Interactive API documentation is available at: http://localhost:5000/docs
   - Alternative API documentation: http://localhost:5000/redoc

### Frontend (React)

The React frontend provides a beautiful, interactive visualization of the building simulation:

#### Running the Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. The web interface will be available at http://localhost:3000

### Features of the Web Interface

- **Building Visualization**: Interactive 3D-like representation of the building with all floors and rooms
- **Real-time Updates**: See the simulation update in real-time
- **Detailed Statistics**: Track the infestation rate and other metrics with charts and graphs
- **Full Control**: All simulation commands available through an intuitive interface
- **Room Selection**: Click on rooms to perform targeted actions like cleaning or resetting sensors
- **Auto-run Mode**: Let the simulation run automatically with a configurable interval

### Deployment

To deploy the application:

1. Build the React frontend:
   ```
   cd frontend
   npm run build
   ```

2. Serve the FastAPI application with a production ASGI server like Uvicorn or Hypercorn:
   ```
   uvicorn src.api:app --host 0.0.0.0 --port 5000
   ```

3. For production deployment, consider using a process manager like Supervisor or PM2, and a reverse proxy like Nginx.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 