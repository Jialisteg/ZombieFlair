# Simulación de Sensores IoT de flair con Zombies

Una aplicación CLI en Python que simula un edificio infestado de zombies, utilizando sensores IoT para rastrear la invasión.

## Descripción

Esta aplicación simula un escenario donde un edificio está infestado de zombies, y se utilizan sensores IoT para detectar su presencia. El usuario puede configurar el edificio, añadir zombies iniciales y simular la propagación de la infestación turno por turno.



## Características

- Configurar un edificio con múltiples pisos y habitaciones
- Añadir zombies iniciales a habitaciones aleatorias
- Simular el movimiento de zombies entre habitaciones adyacentes
- Rastrear el estado de cada habitación y sensor
- Limpiar habitaciones de zombies
- Restablecer sensores que han sido activados
- Uso del ARMA SECRETA 
- Agregar zombies manualmente durante la simulación
- Activar/desactivar la generación automática de zombies
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
   - Opción 2: Agregar otro Zombie - Añade un zombie en una habitación aleatoria
   - Opción 3: Limpiar Habitación - Elimina zombies de una habitación específica
   - Opción 4: Restablecer Sensor - Restablece un sensor al estado normal
   - Opción 5: Activar/Desactivar Generación de zombies - Controla la generación automática
   - Opción 6: Utilizar el ARMA SECRETA (probar)
   - Opción 7: Agregar Practicante - Funcionalidad en desarrollo
   - Opción 8: Volver al menú principal - Regresa al menú principal

## Arquitectura

La aplicación está estructurada utilizando principios de programación orientada a objetos:

- **Edificio (Building)**: Administra una colección de pisos y proporciona métodos para acceder a las habitaciones
- **Piso (Floor)**: Contiene múltiples habitaciones y maneja las conexiones entre ellas
- **Habitación (Room)**: Representa un espacio físico que puede contener zombies y tiene un sensor
- **Escalera (Staircase)**: Un tipo especial de habitación que permite el movimiento vertical entre pisos
- **Sensor**: Detecta la presencia de zombies y puede estar en estado "normal" o "alerta"
- **Practicante**: Representa al interno que se mueve por el edificio y debe ser protegido de los zombies
- **Simulación (Simulation)**: Orquesta la lógica de movimiento de zombies y rastrea el estado del juego
- **ZombieSimulationCLI**: Proporciona la interfaz de línea de comandos para la interacción del usuario

## Estructura del Proyecto

La organización de archivos y carpetas del proyecto es la siguiente:

```
├── README.md             # Documentación del proyecto
├── README_TESTS.md       # Documentación específica para tests
├── run.py                # Punto de entrada para ejecutar la aplicación
├── run_api.py            # Script para ejecutar solo la API
├── setup.py              # Configuración para instalar como paquete Python
├── requirements.txt      # Dependencias para el entorno de Python
├── package.json          # Configuración del proyecto en la raíz
├── Dockerfile            # Configuración para contenedor Docker
├── docker-compose.yml    # Configuración de Docker Compose
├── .gitignore            # Archivos y carpetas ignorados por git
├── api/                  # API independiente para la visualización web
│   ├── index.py          # Punto de entrada para FastAPI
│   ├── requirements.txt  # Dependencias específicas para la API
│   ├── Dockerfile        # Configuración Docker para la API
│   ├── Dockerfile.do     # Configuración Docker para DigitalOcean
│   └── vercel.json       # Configuración para despliegue en Vercel
├── frontend/             # Aplicación React para visualización web
│   ├── src/              # Código fuente de React
│   │   ├── api/          # Configuración de llamadas a la API
│   │   ├── components/   # Componentes de React
│   │   ├── App.js        # Componente principal
│   │   ├── index.js      # Punto de entrada
│   │   └── index.css     # Estilos globales
│   ├── public/           # Archivos estáticos públicos
│   ├── package.json      # Dependencias y scripts para React
│   ├── entrypoint.sh     # Script de entrada para el contenedor
│   ├── Dockerfile        # Configuración Docker para el frontend
│   ├── Dockerfile.do     # Configuración Docker para DigitalOcean
│   ├── nginx.conf        # Configuración de Nginx para producción
│   └── vercel.json       # Configuración para despliegue en Vercel
├── logs/                 # Directorio donde se almacenan los archivos de log
├── src/                  # Código fuente principal de la simulación
│   ├── main.py           # CLI principal para interacción del usuario
│   ├── simulation.py     # Lógica de simulación de zombis
│   ├── api.py            # Conexión entre la simulación y la API
│   ├── logger.py         # Módulo de registro y depuración
│   ├── fix.md            # Documentación sobre las correcciones de interfaz
│   ├── models/           # Modelos de datos para la aplicación
│   │   ├── __init__.py   # Inicializador del paquete models
│   │   ├── building.py   # Clase Edificio
│   │   ├── floor.py      # Clase Piso
│   │   ├── room.py       # Clase Habitación 
│   │   ├── staircase.py  # Clase Escalera (Nueva)
│   │   ├── sensor.py     # Clase Sensor
│   │   └── practicante.py # Clase Practicante (Nueva)
│   └── api/              # Componentes específicos de la API dentro de src
├── tests/                # Pruebas unitarias
│   ├── __init__.py       # Inicializador del paquete tests
│   ├── conftest.py       # Configuración y fixtures para tests
│   ├── test_models.py    # Tests para modelos (Building, Floor, Room, etc.)
│   └── test_simulation.py # Tests para la lógica de simulación
```

### Visualización del Edificio (Versión CLI)

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
- `🧟`: Presencia de zombie
- `🪜`: Escalera
- `🚪`: Puerta (habitación regular)
- `🚨`: Sensor en estado de alerta
- `🟢`: Sensor en estado normal
- `🚶`: Practicante (debe ser protegido de los zombies)

### Lógica de Movimiento de Zombies

- Los zombies se propagan a habitaciones adyacentes en cada turno
- **Movimiento Horizontal**: Las habitaciones se consideran adyacentes si tienen números de habitación consecutivos en el mismo piso
- **Movimiento Vertical**: Los zombies pueden moverse entre pisos ÚNICAMENTE a través de las escaleras (habitación 0 de cada piso)
- Las escaleras permiten a los zombies moverse hacia el piso superior o inferior
- Las escaleras NO tienen sensores, pero permiten la propagación vertical de zombies
- Cuando los zombies entran en una habitación normal, el sensor entra en estado de alerta
- La simulación termina cuando todas las habitaciones están infestadas o un zombie captura al practicante

### Funcionalidades Adicionales

1. **Arma Secreta**:
   - Permite eliminar zombies de varias habitaciones a la vez
   - Cada zombie tiene 50% de probabilidad de ser eliminado
   - Los sensores permanecen en alerta incluso si los zombies son eliminados

2. **Practicante (Interno)**:
   - Simbolizado por el icono 🚶
   - Solo puede haber un practicante a la vez en el edificio
   - Se mueve automáticamente en cada turno a habitaciones adyacentes sin zombies
   - No activa los sensores al entrar en una habitación
   - Si un zombie llega a la misma habitación que el practicante, el juego termina
   - Añade un elemento de estrategia, ya que debes mantenerlo protegido de los zombies

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

## Nueva Funcionalidad: Visualización Web Interactiva

Además de la interfaz CLI, este proyecto ahora incluye una visualización web construida con FastAPI y React.

## Instrucciones para Ejecutar la Aplicación Localmente

### Requisitos Previos

- Python 3.9+
- Node.js 18+
- npm 8+

### Ejecutar el Backend (FastAPI)

1. Navega al directorio api:
   ```bash
   cd api
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta el servidor de desarrollo:
   ```bash
   uvicorn index:app --host 0.0.0.0 --port 5000 --reload
   ```

El backend estará disponible en [http://localhost:5000](http://localhost:5000)

### Ejecutar el Frontend (React)

1. Abre una nueva terminal y navega al directorio frontend:
   ```bash
   cd frontend
   ```

2. Instala las dependencias:
   ```bash
   npm install
   ```

3. Inicia el servidor de desarrollo:
   ```bash
   npm start
   ```

El frontend estará disponible en [http://localhost:3000](http://localhost:3000)

## Verificación de Funcionamiento

1. Verifica el API: Abre [http://localhost:5000/api/simulation/state](http://localhost:5000/api/simulation/state) en tu navegador para comprobar que el API responde correctamente.

2. Usa la interfaz: Abre [http://localhost:3000](http://localhost:3000) para interactuar con la aplicación completa.

## Solución de Problemas Comunes

- **Error "Module not found"**: Asegúrate de que estás ejecutando los comandos desde los directorios correctos.
- **Problemas de conexión entre frontend y backend**: Verifica que el archivo `frontend/src/api/simulationApi.js` esté configurado para usar `http://localhost:5000/api` en desarrollo.

## Opciones de Despliegue

### Vercel

La aplicación está configurada para ser desplegada en Vercel:

1. Frontend:
   - Conecta tu repositorio a Vercel
   - Establece el directorio raíz como "frontend"
   - Framework preset: Create React App

2. Backend:
   - Crea un nuevo proyecto para el backend
   - Establece el directorio raíz como "api"
   - Asegúrate de que el frontend esté configurado para usar la URL correcta del backend

## Estructura del Proyecto

- `api/`: Backend de FastAPI
- `frontend/`: Frontend de React
- `src/`: Código fuente Python de la simulación
- `tests/`: Pruebas automatizadas (Falta por terminar)




## Updates y futuras implementaciones
### Se agregan escaleras para el desplazamiento vertical (en un lugar fijo).

### Se agrega nuevo modo: Salvando a un practicante (en desarrollo)

Un día que fallaron los sensores, se decidió mandar a un pobre practicante al edificio de un cliente muy importante, para poder investigar la falla en cuestión. Ese mismo día comenzó un apocalipsis zombie: En este modo se agrega un practicante al edificio, el cual debe evitar a los zombies. Para ello, decide avanzar e ir escondiéndose en habitaciones. El problema es que en este modo, las puertas se abren de manera automática (como en los malls), a menos que se bloqueen remotamente por sus compañeros de trabajo desde la oficina.

El equipo del practicante deberá entonces bloquear remotamente las puertas de las habitaciones en donde se encuentre el practicante. Usted toma el rol de ingeniero IoT que intentará salvar al practicante utilizando la información de los sensores que se activan cuando los zombies pasan por cada habitación. Si se activa el sensor adyacente al practicante, indica que hay un zombie cerca y el practicante debería esconderse en la habitación, pero se debe tener en cuenta de que el zombie puede entrar a la habitación antes de que las puertas se alcancen a cerrar de manera remota.

- Esconderse en la habitación toma un turno
- Activar el cierre de puertas de manera remota toma dos turnos a partir de que el practicante entra a la habitación. Si el practicante escapa cuando tiene un zombie a una celda de distancia, el zombie alcanzaría a entrar a la habitación. 

### Se modifica la agresividad de los zombies (se mueven de manera random hasta que tienen al practicante a algún rango "n" de distancia y luego van directamente hacia él).

### Se agrega el arma secreta:

Cuando todo está perdido, se agrega un botón de utilizar arma secreta que permitirá cumplir todos los sueños de la empresa, salvar al practicante, triplicar la producción y ganar la felicidad absoluta.