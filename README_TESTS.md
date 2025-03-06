# Pruebas para la Simulación de Zombies

Este directorio contiene pruebas automatizadas para verificar el correcto funcionamiento de la simulación de zombies.

## Requisitos

Para ejecutar las pruebas, necesitas tener instalado:

- Python 3.6 o superior
- pytest y pytest-mock (instalables mediante requirements.txt)

## Instalación

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Ejecutar las pruebas

Para ejecutar todas las pruebas:

```bash
python -m pytest tests/
```

Para ejecutar un archivo de prueba específico:

```bash
python -m pytest tests/test_simulation.py
```

Para ejecutar una prueba específica:

```bash
python -m pytest tests/test_simulation.py::test_zombie_moves_to_one_room_at_a_time
```

Para obtener información detallada sobre las pruebas:

```bash
python -m pytest tests/ -v
```

## Pruebas incluidas

### Simulación (`test_simulation.py`)

- `test_setup_building`: Verifica la correcta configuración del edificio.
- `test_add_initial_zombies`: Verifica la adición inicial de zombies.
- `test_toggle_zombie_generation`: Verifica la activación/desactivación de generación de zombies.
- `test_clean_room`: Verifica la limpieza de zombies de una habitación.
- `test_reset_sensor`: Verifica el restablecimiento de sensores en alerta.
- `test_zombie_moves_to_one_room_at_a_time`: Verifica que los zombies solo se mueven a una habitación a la vez.
- `test_zombie_generation`: Verifica la generación controlada de zombies.
- `test_sensor_alerts_when_zombie_enters_room`: Verifica que los sensores se activan cuando un zombie entra.

### Modelos (`test_models.py`)

- `test_room_creation`: Verifica la creación de habitaciones.
- `test_room_zombie_management`: Verifica la gestión de zombies en una habitación.
- `test_floor_creation`: Verifica la creación de pisos.
- `test_floor_room_access`: Verifica el acceso a habitaciones en un piso.
- `test_building_creation`: Verifica la creación del edificio.
- `test_building_floor_access`: Verifica el acceso a pisos en un edificio.
- `test_building_room_access`: Verifica el acceso a habitaciones a través del edificio.

### CLI (`test_cli.py`)

- `test_cli_initialization`: Verifica la inicialización de la interfaz de línea de comandos.

## Agregar nuevas pruebas

Para agregar nuevas pruebas, sigue estos pasos:

1. Identifica el componente que deseas probar.
2. Crea una nueva función de prueba en el archivo correspondiente.
3. Usa fixtures para crear objetos reutilizables.
4. Realiza aserciones para verificar el comportamiento esperado. 