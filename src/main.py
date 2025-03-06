#!/usr/bin/env python3
import os
import sys
import time
from src.simulation import Simulation
from src import logger

class ZombieSimulationCLI:
    """
    Interfaz de línea de comandos para la Simulación de Sensores IoT con Zombis.
    """
    
    def __init__(self):
        """Inicializa el CLI con una nueva simulación."""
        self.simulation = Simulation()
        self.running = True
        logger.debug("CLI inicializado")
    
    def clear_screen(self):
        """Limpia la pantalla del terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Imprime el encabezado de la aplicación."""
        self.clear_screen()
        print("=" * 80)
        print("🧟 SIMULACIÓN DE SENSORES IOT CON ZOMBIS 🧟".center(80))
        if logger.is_debug_enabled():
            print("🔍 MODO DEBUG ACTIVADO 🔍".center(80))
        print("=" * 80)
        print()
    
    def print_building_state(self):
        """Imprime el estado actual del edificio."""
        if not self.simulation.building:
            print("No hay edificio configurado todavía. Use la opción 1 para configurar un edificio.")
            return
        
        state = self.simulation.get_building_state()
        
        print(f"\nTurno: {state['turn']}")
        print(f"Estado del Edificio: {state['infested_rooms']}/{state['total_rooms']} habitaciones infestadas")
        print("  Por piso:")
        for floor_idx, floor in enumerate(self.simulation.building.floors):
            zombie_rooms = floor.get_rooms_with_zombies()
            total_rooms = len(floor.get_rooms())
            percentage = (len(zombie_rooms) / total_rooms) * 100 if total_rooms > 0 else 0
            print(f"    - Piso {floor_idx}: {len(zombie_rooms)}/{total_rooms} habitaciones infestadas ({percentage:.1f}%)")
            
            # Si estamos en modo DEBUG, mostrar las habitaciones específicas infestadas
            if logger.is_debug_enabled() and zombie_rooms:
                room_numbers = [room.room_number for room in zombie_rooms]
                room_numbers.sort()
                print(f"      Habitaciones infestadas: {', '.join(map(str, room_numbers))}")
        
        print()
        
        # Imprimir cada piso y sus habitaciones, empezando por el piso más alto
        for floor_idx in range(len(self.simulation.building.floors) - 1, -1, -1):
            floor = self.simulation.building.get_floor(floor_idx)
            print(f"Piso {floor_idx}:")
            
            # Imprimir habitaciones en formato de cuadrícula
            rooms_per_row = 5
            rooms = floor.get_rooms()
            
            for i in range(0, len(rooms), rooms_per_row):
                row_rooms = rooms[i:i+rooms_per_row]
                
                # Imprimir números de habitación
                print("  ", end="")
                for j, room in enumerate(row_rooms):
                    room_type = "Esc" if hasattr(room, 'connected_floors') else "Hab"
                    print(f"{room_type} {room.room_number}", end="")
                    if j < len(row_rooms) - 1:
                        print("          ", end="")
                print()
                
                # Imprimir todos los datos en un solo formato simplificado
                print("  ", end="")
                for j, room in enumerate(row_rooms):
                    # Determinar los elementos visuales
                    zombie = "🧟" if room.has_zombies else "  "
                    icon = "🪜" if hasattr(room, 'connected_floors') else "🚪"
                    
                    # Determinar el sensor (las escaleras no tienen sensor)
                    if hasattr(room, 'connected_floors'):
                        sensor = "  "  # No hay sensor
                    else:
                        sensor = "🚨" if room.sensor.is_alert() else "🟢"
                    
                    # Imprimir todo en un único formato compacto
                    print(f"[{zombie} {icon} {sensor}]", end="")
                    
                    # Añadir espaciado entre elementos
                    if j < len(row_rooms) - 1:
                        print("     ", end="")
                print("\n")
            
            print()
        
        if self.simulation.is_game_over():
            print("\n🚨 FIN DEL JUEGO: ¡Todas las habitaciones han sido infestadas con zombis! 🚨\n")
    
    def setup_building(self):
        """Configura un nuevo edificio para la simulación."""
        self.print_header()
        print("CONFIGURACIÓN DEL EDIFICIO")
        print("-" * 80)
        print("(Escriba 'salir' para volver al menú principal en cualquier momento)")
        
        # Obtener número de pisos
        while True:
            floors_input = input("\nIngrese número de pisos: ")
            
            if floors_input.lower() == 'salir':
                return
                
            try:
                floors_count = int(floors_input)
                if floors_count <= 0:
                    print("Error: El número de pisos debe ser positivo.")
                    continue
                break
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")
        
        # Obtener número de habitaciones por piso
        while True:
            rooms_input = input("\nIngrese número de habitaciones regulares por piso (sin contar la escalera): ")
            
            if rooms_input.lower() == 'salir':
                return
                
            try:
                rooms_per_floor = int(rooms_input)
                if rooms_per_floor <= 0:
                    print("Error: El número de habitaciones debe ser positivo.")
                    continue
                break
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")
        
        result = self.simulation.setup_building(floors_count, rooms_per_floor)
        
        print(f"\nConfiguración:\n- {floors_count} pisos")
        print(f"- {rooms_per_floor} habitaciones regulares por piso (+ 1 escalera)")
        print(f"- Total de espacios: {result['total_rooms']} ({result['normal_rooms']} habitaciones + {result['staircases']} escaleras)")
        
        # Añadir zombis iniciales
        while True:
            zombies_input = input("\nIngrese número de zombis iniciales: ")
            
            if zombies_input.lower() == 'salir':
                return
                
            try:
                zombie_count = int(zombies_input)
                if zombie_count <= 0:
                    print("Error: El número de zombis debe ser positivo.")
                    continue
                break
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")
        
        self.simulation.add_initial_zombies(zombie_count)
        
        print("\n¡Configuración del edificio completada!")
        input("Presione Enter para continuar...")
    
    def advance_simulation(self):
        """Avanza la simulación en un turno."""
        if not self.simulation.building:
            self.print_header()
            print("No hay edificio configurado todavía. Use la opción 1 para configurar un edificio.")
            input("Presione Enter para continuar...")
            return
        
        while True:
            result = self.simulation.advance_turn()
            
            self.print_header()
            self.print_building_state()
            
            if "error" in result:
                print(f"Error: {result['error']}")
                logger.error(f"Error al avanzar turno: {result['error']}")
            else:
                print(f"\nTurno {result['turn']} completado.")
                if result['newly_infested']:
                    print(f"Movimientos de zombis: {len(result['newly_infested'])}")
                    if logger.is_debug_enabled():
                        for i, (floor, room) in enumerate(result['newly_infested']):
                            from_floor, from_room = result['vacated_rooms'][i]
                            print(f"  - Zombi movido: ({from_floor},{from_room}) → ({floor},{room})")
                else:
                    print("No hubo movimiento de zombis en este turno.")
                    
                if result['new_zombie_generated']:
                    print("¡Se ha generado un nuevo zombi en una habitación aleatoria!")
                print(f"Total de habitaciones infestadas: {result['total_infested']}")
                
                if result['game_over']:
                    print("\n🚨 FIN DEL JUEGO: ¡Todas las habitaciones han sido infestadas con zombis! 🚨")
            
            # Dar opciones al usuario
            print("\nMENÚ DE JUEGO")
            print("-" * 80)
            print("1. Avanzar otro turno (funciona con enter también)")
            print("2. Agregar otro Zombie")
            print("3. Limpiar Habitación (Eliminar Zombis)")
            print("4. Restablecer Sensor")
            print("5. Activar/Desactivar Generación de Zombis")
            print("6. Utilizar el arma secreta")
            print("7. Agregar Practicante")
            print("8. Volver al menú principal")
            
            choice = input("\nIngrese su opción (1-8): ")
            
            if choice == "8":
                break
            elif choice == "2":
                # Agregar un zombie aleatorio
                added = self.simulation.add_random_zombie()
                if added:
                    print("\n¡Se ha agregado un nuevo zombi en una habitación aleatoria!")
                else:
                    print("\nNo se pudo agregar un nuevo zombi (todas las habitaciones podrían estar infestadas).")
                input("\nPresione Enter para continuar...")
            elif choice == "3":
                self.clean_room()
            elif choice == "4":
                self.reset_sensor()
            elif choice == "5":
                enabled = self.simulation.toggle_zombie_generation()
                if enabled:
                    print("\n🧟 Generación de zombis ACTIVADA 🧟")
                    print("Se generará un nuevo zombi aleatorio en cada turno.")
                else:
                    print("\n🧟 Generación de zombis DESACTIVADA 🧟")
                    print("No se generarán nuevos zombis durante la simulación.")
                input("\nPresione Enter para continuar...")
            elif choice == "6":
                # Utilizar arma secreta (elimina zombis de varias habitaciones)
                cleaned_count = self.simulation.use_secret_weapon()
                if cleaned_count > 0:
                    print(f"\n¡BOOM! El arma secreta ha eliminado zombis de {cleaned_count} habitaciones.")
                else:
                    print("\nEl arma secreta no tuvo efecto. No había zombis para eliminar.")
                input("\nPresione Enter para continuar...")
            elif choice == "7":
                # Agregar Practicante (funcionalidad por implementar)
                print("\nOpción en desarrollo. Funcionalidad por implementar.")
                input("\nPresione Enter para continuar...")
            else:
                # Opción 1 o Enter (continuar)
                pass
    
    def clean_room(self):
        """Limpia los zombis de una habitación específica."""
        if not self.simulation.building:
            self.print_header()
            print("No hay edificio configurado todavía. Use la opción 1 para configurar un edificio.")
            input("Presione Enter para continuar...")
            return
        
        self.print_header()
        self.print_building_state()
        
        print("\nLIMPIAR HABITACIÓN (ELIMINAR ZOMBIS)")
        print("-" * 80)
        
        try:
            floor_number = int(input("Ingrese número de piso: "))
            room_number = int(input("Ingrese número de habitación: "))
            
            # Validar que no sea una escalera (habitación 0)
            if room_number == 0:
                print("\nError: No se pueden limpiar las escaleras (habitación 0).")
                input("\nPresione Enter para continuar...")
                return
            
            result = self.simulation.clean_room(floor_number, room_number)
            
            if "error" in result:
                print(f"\nError: {result['error']}")
            elif result["cleaned"]:
                print(f"\nLa habitación {floor_number}-{room_number} ha sido limpiada. Los zombis han sido eliminados.")
                print("Nota: El sensor permanecerá en alerta hasta que se restablezca manualmente.")
            else:
                print(f"\n{result['message']}")
            
            input("\nPresione Enter para continuar...")
            
        except ValueError:
            print("Por favor, ingrese números válidos.")
            logger.warning("Valores inválidos ingresados durante la limpieza de habitación")
            input("Presione Enter para continuar...")
    
    def reset_sensor(self):
        """Restablece un sensor en una habitación específica."""
        if not self.simulation.building:
            self.print_header()
            print("No hay edificio configurado todavía. Use la opción 1 para configurar un edificio.")
            input("Presione Enter para continuar...")
            return
        
        self.print_header()
        self.print_building_state()
        
        print("\nRESTABLECER SENSOR")
        print("-" * 80)
        
        try:
            floor_number = int(input("Ingrese número de piso: "))
            room_number = int(input("Ingrese número de habitación: "))
            
            # Validar que no sea una escalera (habitación 0)
            if room_number == 0:
                print("\nError: Las escaleras (habitación 0) no tienen sensores.")
                input("\nPresione Enter para continuar...")
                return
            
            result = self.simulation.reset_sensor(floor_number, room_number)
            
            if "error" in result:
                print(f"\nError: {result['error']}")
            elif result["reset"]:
                print(f"\nEl sensor en la habitación {floor_number}-{room_number} ha sido restablecido.")
            else:
                print(f"\n{result['message']}")
            
            input("\nPresione Enter para continuar...")
            
        except ValueError:
            print("Por favor, ingrese números válidos.")
            logger.warning("Valores inválidos ingresados durante el restablecimiento del sensor")
            input("Presione Enter para continuar...")
    
    def toggle_debug_mode(self):
        """Activa o desactiva el modo de depuración."""
        new_state = not logger.is_debug_enabled()
        logger.set_debug_mode(new_state)
        
        self.print_header()
        if new_state:
            print("🔍 Modo DEBUG ACTIVADO 🔍")
            print("Los mensajes de depuración se mostrarán en la consola y se guardarán en el archivo de log.")
        else:
            print("🔍 Modo DEBUG DESACTIVADO 🔍")
            print("Solo los mensajes de error se mostrarán en la consola, pero todos los niveles se guardarán en el archivo de log.")
        
        input("\nPresione Enter para continuar...")
    
    def show_debug_info(self):
        """Muestra información de depuración si el modo DEBUG está activado."""
        if not logger.is_debug_enabled():
            self.print_header()
            print("El modo DEBUG está desactivado. Active el modo DEBUG primero.")
            input("\nPresione Enter para continuar...")
            return
            
        self.print_header()
        print("INFORMACIÓN DE DEPURACIÓN")
        print("-" * 80)
        
        # Mostrar información básica
        print(f"Archivo de log: {logger.log_file}")
        print(f"Modo DEBUG: {'Activado' if logger.is_debug_enabled() else 'Desactivado'}")
        
        # Mostrar información de la simulación
        if self.simulation.building:
            state = self.simulation.get_building_state()
            print("\nEstado de la simulación:")
            for key, value in state.items():
                print(f"  - {key}: {value}")
            
            # Mostrar información detallada de los pisos
            print("\nInformación detallada de pisos:")
            for floor_idx, floor in enumerate(self.simulation.building.floors):
                zombie_rooms = floor.get_rooms_with_zombies()
                print(f"  - Piso {floor_idx}: {len(zombie_rooms)}/{len(floor.rooms)} habitaciones infestadas")
        else:
            print("\nNo hay edificio configurado.")
            
        input("\nPresione Enter para continuar...")
    
    def show_menu(self):
        """Muestra el menú principal y obtiene la entrada del usuario."""
        self.print_header()
        
        if self.simulation.building:
            self.print_building_state()
            
            # Mostrar leyenda de íconos
            print("\nLEYENDA:")
            print("🚪 : Habitación normal")
            print("🪜 : Escalera (permite movimiento entre pisos)")
            print("🧟 : Zombi")
            print("🚨 : Sensor en alerta")
            print("🟢 : Sensor normal")
        
        print("\nMENÚ PRINCIPAL")
        print("-" * 80)
        print("0. Instrucciones del Juego")
        print("1. Configurar Edificio")
        print("2. Comenzar Simulación")
        print("3. Activar/Desactivar modo DEBUG")
        if logger.is_debug_enabled():
            print("4. Mostrar información de depuración")
        print("5. Salir")
        
        max_option = 5
        
        choice = input(f"\nIngrese su opción (0-{max_option}): ")
        
        if choice == "0":
            self.show_welcome_screen()
        elif choice == "1":
            self.setup_building()
        elif choice == "2":
            # Comenzar Simulación
            if not self.simulation.building:
                print("\nNo hay edificio configurado todavía. Redirigiendo a Configurar Edificio...")
                time.sleep(2)
                self.setup_building()
            else:
                self.advance_simulation()
        elif choice == "3":
            self.toggle_debug_mode()
        elif choice == "4" and logger.is_debug_enabled():
            self.show_debug_info()
        elif choice == "5":
            self.running = False
            print("\n¡Gracias por usar la Simulación de Sensores IoT con Zombis!")
            logger.info("Aplicación terminada por el usuario")
            time.sleep(1)
        else:
            print("\nOpción inválida. Por favor, intente de nuevo.")
            input("Presione Enter para continuar...")
    
    def show_welcome_screen(self):
        """Muestra la pantalla de bienvenida con las instrucciones del juego."""
        self.print_header()
        print("¡Bienvenido a la Simulación de Sensores IoT con Zombis!")
        print("\nINSTRUCCIONES DEL JUEGO")
        print("-" * 80)
        print("En esta simulación, usted administrará un edificio infestado de zombis utilizando")
        print("sensores IoT de Flair de última generación. Aquí está lo que necesita saber:")
        print("\n1. CONFIGURACIÓN:")
        print("   - Primero, configure el edificio especificando el número de pisos y habitaciones.")
        print("   - Cada piso tendrá automáticamente una escalera (habitación 0) más las habitaciones regulares que especifique.")
        print("   - Luego, indique cuántos zombies iniciales habrá en el edificio.")
        print("\n2. VISUALIZACIÓN:")
        print("   - 🚪 = Habitación normal")
        print("   - 🪜 = Escalera (permite movimiento entre pisos)")
        print("   - 🧟 = Habitación con zombies")
        print("   - 🚨 = Sensor Flair en estado de alerta")
        print("   - 🟢 = Sensor Flair en estado normal")
        print("\n3. MECÁNICA DEL JUEGO:")
        print("   - Los zombies se propagan a habitaciones adyacentes en cada turno.")
        print("   - Movimiento horizontal: Los zombies se mueven entre habitaciones del mismo piso.")
        print("   - Movimiento vertical: Los zombies pueden moverse entre pisos ÚNICAMENTE usando")
        print("     las escaleras (habitación 0 de cada piso, marcada con 🪜  ).")
        print("   - Las escaleras NO tienen sensores (faltó presupuesto), pero permiten a los zombies moverse arriba/abajo.")
        print("   - Puede limpiar habitaciones de zombies y restablecer sensores.")
        print("   - El juego termina cuando todas las habitaciones están infestadas.")
        print("\n4. CARACTERÍSTICAS ESPECIALES:")
        print("   - Modo DEBUG disponible para ver información detallada.")
        print("   - Los eventos se registran en archivos de log para su revisión.")
        print("\nPara comenzar, seleccione la opción 1 en el menú principal para configurar el edificio.")
        print("-" * 80)
        input("\nPresione Enter para continuar...")

    def toggle_zombie_generation(self):
        """Activa o desactiva la generación aleatoria de zombis."""
        if not self.simulation.building:
            self.print_header()
            print("No hay edificio configurado todavía. Use la opción 1 para configurar un edificio.")
            input("Presione Enter para continuar...")
            return
            
        enabled = self.simulation.toggle_zombie_generation()
        self.print_header()
        if enabled:
            print("🧟 Generación de zombis ACTIVADA 🧟")
            print("Se generará un nuevo zombi aleatorio en cada turno.")
        else:
            print("🧟 Generación de zombis DESACTIVADA 🧟")
            print("No se generarán nuevos zombis durante la simulación.")
        input("\nPresione Enter para continuar...")

    def run(self):
        """Ejecuta el bucle principal de la aplicación."""
        try:
            # Mostrar pantalla de bienvenida al inicio
            self.show_welcome_screen()
            
            while self.running:
                self.show_menu()
        except KeyboardInterrupt:
            print("\n\nAplicación interrumpida por el usuario.")
            logger.info("Aplicación interrumpida por el usuario (KeyboardInterrupt)")
        except Exception as e:
            print(f"\n\nError inesperado: {str(e)}")
            logger.critical(f"Error inesperado: {str(e)}\nTraceback:\n{sys.exc_info()[2]}")
        finally:
            print("\n¡Gracias por usar la Simulación de Sensores IoT con Zombis!")


if __name__ == "__main__":
    app = ZombieSimulationCLI()
    app.run() 