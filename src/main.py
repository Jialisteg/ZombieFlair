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
        print()
        
        # Imprimir cada piso y sus habitaciones
        for floor_idx in range(len(self.simulation.building.floors)):
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
                    print(f"Hab {room.room_number}".ljust(15), end="")
                print()
                
                # Imprimir estado de zombis
                print("  ", end="")
                for room in row_rooms:
                    status = "🧟" if room.has_zombies else "  "
                    print(f"[{status}]".ljust(15), end="")
                print()
                
                # Imprimir estado del sensor
                print("  ", end="")
                for room in row_rooms:
                    sensor = "🚨" if room.sensor.is_alert() else "🟢"
                    print(f"({sensor})".ljust(15), end="")
                print("\n")
            
            print()
        
        if self.simulation.is_game_over():
            print("\n🚨 FIN DEL JUEGO: ¡Todas las habitaciones han sido infestadas con zombis! 🚨\n")
    
    def setup_building(self):
        """Configura un nuevo edificio para la simulación."""
        self.print_header()
        print("CONFIGURACIÓN DEL EDIFICIO")
        print("-" * 80)
        
        try:
            floors_count = int(input("Ingrese número de pisos: "))
            if floors_count <= 0:
                print("El número de pisos debe ser positivo.")
                input("Presione Enter para continuar...")
                return
            
            rooms_per_floor = int(input("Ingrese número de habitaciones por piso: "))
            if rooms_per_floor <= 0:
                print("El número de habitaciones debe ser positivo.")
                input("Presione Enter para continuar...")
                return
            
            self.simulation.setup_building(floors_count, rooms_per_floor)
            
            # Añadir zombis iniciales
            zombie_count = int(input("Ingrese número de zombis iniciales: "))
            if zombie_count <= 0:
                print("El número de zombis debe ser positivo.")
                input("Presione Enter para continuar...")
                return
            
            self.simulation.add_initial_zombies(zombie_count)
            
            print("\n¡Configuración del edificio completada!")
            input("Presione Enter para continuar...")
            
        except ValueError:
            print("Por favor, ingrese números válidos.")
            logger.warning("Valores inválidos ingresados durante la configuración del edificio")
            input("Presione Enter para continuar...")
    
    def advance_simulation(self):
        """Avanza la simulación en un turno."""
        if not self.simulation.building:
            self.print_header()
            print("No hay edificio configurado todavía. Use la opción 1 para configurar un edificio.")
            input("Presione Enter para continuar...")
            return
        
        result = self.simulation.advance_turn()
        
        self.print_header()
        self.print_building_state()
        
        if "error" in result:
            print(f"Error: {result['error']}")
            logger.error(f"Error al avanzar turno: {result['error']}")
        else:
            print(f"\nTurno {result['turn']} completado.")
            print(f"Habitaciones recién infestadas: {len(result['newly_infested'])}")
            print(f"Total de habitaciones infestadas: {result['total_infested']}")
            
            if result['game_over']:
                print("\n🚨 FIN DEL JUEGO: ¡Todas las habitaciones han sido infestadas con zombis! 🚨")
        
        input("\nPresione Enter para continuar...")
    
    def clean_room(self):
        """Limpia los zombis de una habitación específica."""
        if not self.simulation.building:
            self.print_header()
            print("No hay edificio configurado todavía. Use la opción 1 para configurar un edificio.")
            input("Presione Enter para continuar...")
            return
        
        self.print_header()
        self.print_building_state()
        
        print("\nLIMPIAR HABITACIÓN")
        print("-" * 80)
        
        try:
            floor_number = int(input("Ingrese número de piso: "))
            room_number = int(input("Ingrese número de habitación: "))
            
            if self.simulation.clean_room(floor_number, room_number):
                print(f"\nLa habitación {floor_number}-{room_number} ha sido limpiada de zombis.")
            else:
                print(f"\nNo se pudo limpiar la habitación {floor_number}-{room_number}. Verifique si existe y tiene zombis.")
            
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
            
            if self.simulation.reset_sensor(floor_number, room_number):
                print(f"\nEl sensor en la habitación {floor_number}-{room_number} ha sido restablecido.")
            else:
                print(f"\nNo se pudo restablecer el sensor en la habitación {floor_number}-{room_number}. Verifique si existe.")
            
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
        
        print("\nMENÚ PRINCIPAL")
        print("-" * 80)
        print("1. Configurar Edificio")
        print("2. Mostrar Estado del Edificio")
        print("3. Avanzar Simulación (Siguiente Turno)")
        print("4. Limpiar Habitación (Eliminar Zombis)")
        print("5. Restablecer Sensor")
        print("6. Activar/Desactivar modo DEBUG")
        if logger.is_debug_enabled():
            print("7. Mostrar información de depuración")
        print("8. Salir")
        
        max_option = 8
        
        choice = input(f"\nIngrese su opción (1-{max_option}): ")
        
        if choice == "1":
            self.setup_building()
        elif choice == "2":
            self.print_header()
            self.print_building_state()
            input("\nPresione Enter para continuar...")
        elif choice == "3":
            self.advance_simulation()
        elif choice == "4":
            self.clean_room()
        elif choice == "5":
            self.reset_sensor()
        elif choice == "6":
            self.toggle_debug_mode()
        elif choice == "7" and logger.is_debug_enabled():
            self.show_debug_info()
        elif choice == "8":
            self.running = False
            print("\n¡Gracias por usar la Simulación de Sensores IoT con Zombis!")
            logger.info("Aplicación terminada por el usuario")
            time.sleep(1)
        else:
            print("\nOpción inválida. Por favor, intente de nuevo.")
            input("Presione Enter para continuar...")
    
    def run(self):
        """Ejecuta el bucle principal de la aplicación."""
        try:
            while self.running:
                self.show_menu()
        except KeyboardInterrupt:
            print("\n\nAplicación interrumpida por el usuario.")
            logger.info("Aplicación interrumpida por el usuario (KeyboardInterrupt)")
        except Exception as e:
            print(f"\n\nError inesperado: {str(e)}")
            logger.critical(f"Error inesperado: {str(e)}", exc_info=True)
        finally:
            print("\n¡Gracias por usar la Simulación de Sensores IoT con Zombis!")


if __name__ == "__main__":
    app = ZombieSimulationCLI()
    app.run() 