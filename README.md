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
   - Opción 6: Salir - Salir de la aplicación

## Arquitectura

La aplicación está estructurada utilizando principios de programación orientada a objetos:

- **Edificio (Building)**: Administra una colección de pisos y proporciona métodos para acceder a las habitaciones
- **Piso (Floor)**: Contiene múltiples habitaciones y maneja las conexiones entre ellas
- **Habitación (Room)**: Representa un espacio físico que puede contener zombis y tiene un sensor
- **Sensor**: Detecta la presencia de zombis y puede estar en estado "normal" o "alerta"
- **Simulación (Simulation)**: Orquesta la lógica de movimiento de zombis y rastrea el estado del juego
- **ZombieSimulationCLI**: Proporciona la interfaz de línea de comandos para la interacción del usuario

### Lógica de Movimiento de Zombis

- Los zombis se propagan a habitaciones adyacentes en cada turno
- Las habitaciones se consideran adyacentes si tienen números de habitación consecutivos en el mismo piso
- Las habitaciones también están conectadas verticalmente entre pisos (mismo número de habitación en diferentes pisos)
- Cuando los zombis entran en una habitación, el sensor entra en estado de alerta
- La simulación termina cuando todas las habitaciones están infestadas

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 