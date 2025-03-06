# Enunciado: Simulación con Sensores IoT en un Edificio Infestado de Zombis

Imagina que despiertas una mañana y descubres que tu edificio está **infestado de zombis**. Afortunadamente, dispones de un **sistema de Sensores IoT** de última generación que te ayudarán a controlar (o al menos, a rastrear) la invasión. 

Tu **misión**: desarrollar una aplicación en **Python**, utilizando **solo la consola** (CLI), que simule esta crisis zombi y permita a un usuario interactuar con la escena para (intentar) mantener la situación bajo control.

---

### 1. Objetivo

1. **Modelar un edificio**: con varios pisos y habitaciones, cada una con un **sensor IoT**.
2. **Detectar zombis**: cuando los zombis lleguen a una habitación, el **sensor** debe pasar a estado de alerta.
3. **Simular turnos**: permitir que los zombis se muevan entre habitaciones adyacentes y se registre la invasión.
4. **Interactuar vía consola**: el usuario debe poder configurar el edificio, ver el estado actual y avanzar la simulación.

### 2. Requisitos Mínimos

1. **Clases / Estructura Recomendada**
    - `Building`: Administra un conjunto de `Floor`.
    - `Floor`: Administra un conjunto de `Room`.
    - `Room`: Indica si hay zombis y contiene un `Sensor`.
    - `Sensor`: Puede estar en diferentes estados (p.ej. `normal`, `alert`).
    - `Simulation`: Orquesta la lógica de la **propagación zombi** y muestra el estado general.
    
    > Nota: Puedes utilizar la estructura base que te entregamos o modificarla a tu antojo. Lo importante es tener un código organizado y comprensible.
    > 
2. **Funciones Básicas**
    - **Configurar edificio**: Permitir inicializar el número de pisos y de habitaciones por piso.
    - **Mostrar estado**: Reportar en consola qué habitaciones tienen zombis, y en qué estado está cada sensor.
    - **Simulación**:
        - El usuario puede “avanzar un turno”.
        - Al hacerlo, los zombis **se mueven** a habitaciones adyacentes (defínelo con tu lógica).
        - Al entrar en una habitación, el sensor de esa habitación se pone en `alert`.
    - **Interactuar**: Un menú o comandos de consola para realizar las acciones anteriores.
3. **Lógica de Movimiento (Ejemplo)**
    - **Habitaciones adyacentes** en el **mismo piso** pueden ser las que tengan `room_number` contiguo (p.ej. habitación 0 es adyacente a la 1).
    - **Entre pisos** (opcional), la habitación n del piso X puede ser adyacente a la habitación n del piso X+1.
    - Cada turno, recorre cada habitación con zombis y “expándelos” a las habitaciones adyacentes.
        - Decide si los zombis también se quedan en la habitación original (expansión) o se mueven completamente (traslado).
    - Cuando los zombis entren a una nueva habitación, el sensor pasa a `alert`.
4. **Interfaz por Consola**
    - Diseña un **menú** o un sistema de **comandos** simples:
        1. Configurar edificio (p.ej. `floors_count`, `rooms_per_floor`).
        2. Mostrar estado del edificio (piso por piso, habitación por habitación).
        3. Avanzar la simulación (mover los zombis).
        4. (Opcional) Limpiar habitación / Bloquear habitación / Resetear sensor.
        5. Salir.
5. **Buenas Prácticas y Legibilidad**
    - Si lo deseas, añade un archivo de **persistencia** (p.ej., JSON) para guardar y cargar el estado, pero **no es obligatorio**.
    - Cualquier otra cosa que se te ocurra.

---

### 3. Entrega

1. **Repositorio o Archivo Comprimido**
    - Sube tu solución a GitHub/GitLab o envíala en un `.zip`.
2. **README**
    - Explica en pocas líneas **cómo** instalar y **ejecutar** tu aplicación.
    - Describe tu **arquitectura** y/o las clases que creaste.
    - Indica los **comandos** o instrucciones para usar la aplicación (p.ej. menú de opciones).

---

Sobre cualquier cosa haz todos los supuestos que creas necesarios. Obviamente puedes usar cualquier herramienta que quieras. Mucho éxito y gracias por postular :)

Una vez nos envies la tarea te contactaremos para continuar el proceso.