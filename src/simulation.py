import random
from src.models.building import Building
from src import logger

class Simulation:
    """
    Gestiona la simulación de zombis, incluyendo el movimiento de zombis y el estado del juego.
    """
    
    def __init__(self):
        """Inicializa la simulación."""
        self.building = None
        self.turn = 0
        self.zombie_generation_enabled = False
        logger.info("Simulación inicializada")
    
    def toggle_zombie_generation(self):
        """Activa o desactiva la generación aleatoria de zombis."""
        self.zombie_generation_enabled = not self.zombie_generation_enabled
        status = "activada" if self.zombie_generation_enabled else "desactivada"
        logger.info(f"Generación de zombis {status}")
        return self.zombie_generation_enabled
    
    def generate_random_zombie(self):
        """Genera un nuevo zombi en una habitación aleatoria que no tenga zombis."""
        if not self.building:
            return False

        # Obtener todas las habitaciones sin zombis
        available_rooms = []
        for floor_idx, floor in enumerate(self.building.floors):
            for room_idx, room in enumerate(floor.get_rooms()):
                if not room.has_zombies:
                    available_rooms.append((floor_idx, room_idx))

        if not available_rooms:
            logger.debug("No hay habitaciones disponibles para generar un nuevo zombi")
            return False

        # Seleccionar una habitación aleatoria
        floor_idx, room_idx = random.choice(available_rooms)
        room = self.building.get_floor(floor_idx).get_room(room_idx)
        room.has_zombies = True
        room.sensor.set_alert()  # Activar el sensor cuando se añade un zombi
        logger.debug(f"Nuevo zombi generado en piso {floor_idx}, habitación {room_idx}")
        return True
    
    def setup_building(self, floors_count, rooms_per_floor):
        """
        Configura un nuevo edificio para la simulación.
        
        Args:
            floors_count (int): El número de pisos en el edificio
            rooms_per_floor (int): El número de habitaciones en cada piso
        """
        logger.info(f"Configurando edificio: {floors_count} pisos, {rooms_per_floor} habitaciones por piso")
        self.building = Building(floors_count, rooms_per_floor)
        self.turn = 0
        logger.debug("Edificio configurado correctamente")
        return self.building
    
    def add_initial_zombies(self, count=1):
        """
        Añade zombis iniciales en habitaciones aleatorias.
        
        Args:
            count (int): Número de zombis iniciales a añadir
            
        Returns:
            list: Lista de ubicaciones de zombis añadidos
        """
        if not self.building:
            logger.warning("Intento de añadir zombis sin edificio configurado")
            return []
            
        logger.info(f"Añadiendo {count} zombis iniciales")
        zombies_added = []
        
        all_rooms = [(floor_idx, room_idx) 
                    for floor_idx, floor in enumerate(self.building.floors)
                    for room_idx, _ in enumerate(floor.get_rooms())]
        
        # Elegir ubicaciones aleatorias para los zombis
        locations = random.sample(all_rooms, min(count, len(all_rooms)))
        
        for floor_idx, room_idx in locations:
            room = self.building.get_floor(floor_idx).get_room(room_idx)
            room.has_zombies = True
            room.sensor.set_alert()  # Activar el sensor cuando se añade un zombi
            zombies_added.append((floor_idx, room_idx))
            logger.debug(f"Zombi añadido en piso {floor_idx}, habitación {room_idx}")
            
        return zombies_added
    
    def advance_turn(self):
        """Avanza la simulación un turno."""
        if not self.building:
            return {"error": "No hay edificio configurado"}

        self.turn += 1
        logger.debug(f"Iniciando turno {self.turn}")

        # Lista para almacenar las habitaciones recién infestadas y las que perdieron zombis
        newly_infested = []
        vacated_rooms = []
        new_zombie_generated = False

        # Para cada piso y habitación con zombis, mover el zombi a UNA habitación adyacente
        zombie_movements = []  # Lista para guardar los movimientos a realizar

        for floor_idx, floor in enumerate(self.building.floors):
            rooms = floor.get_rooms()
            for room_idx, room in enumerate(rooms):
                if room.has_zombies:
                    # Obtener posibles movimientos (habitaciones adyacentes sin zombis)
                    possible_moves = []
                    
                    # Habitaciones adyacentes horizontales
                    for adj_idx in [room_idx - 1, room_idx + 1]:
                        if 0 <= adj_idx < len(rooms) and not rooms[adj_idx].has_zombies:
                            possible_moves.append((floor_idx, adj_idx))
                    
                    # Habitaciones adyacentes verticales (por las escaleras)
                    if room_idx == 0:  # Solo si el zombi está en la habitación con escaleras
                        for adj_floor in [floor_idx - 1, floor_idx + 1]:
                            if 0 <= adj_floor < len(self.building.floors):
                                if not self.building.get_floor(adj_floor).get_room(0).has_zombies:
                                    possible_moves.append((adj_floor, 0))
                    
                    # Si hay movimientos posibles, elegir uno al azar
                    if possible_moves:
                        target_floor, target_room = random.choice(possible_moves)
                        # Guardar este movimiento para ejecutarlo después
                        zombie_movements.append({
                            'from': (floor_idx, room_idx),
                            'to': (target_floor, target_room)
                        })

        # Ejecutar los movimientos (después de decidir todos para evitar interferencias)
        for move in zombie_movements:
            from_floor, from_room = move['from']
            to_floor, to_room = move['to']
            
            # Obtener las habitaciones
            source_room = self.building.get_floor(from_floor).get_room(from_room)
            target_room = self.building.get_floor(to_floor).get_room(to_room)
            
            # Mover el zombi
            source_room.has_zombies = False
            target_room.has_zombies = True
            target_room.sensor.set_alert()  # Activar el sensor de la nueva habitación
            
            # Registrar el cambio
            vacated_rooms.append((from_floor, from_room))
            newly_infested.append((to_floor, to_room))
            
            logger.debug(f"Zombi movido de piso {from_floor}, habitación {from_room} a piso {to_floor}, habitación {to_room}")

        # Generar un nuevo zombi si está activada la generación
        if self.zombie_generation_enabled:
            new_zombie_generated = self.generate_random_zombie()

        # Verificar si todas las habitaciones están infestadas
        total_infested = sum(1 for floor in self.building.floors 
                           for room in floor.get_rooms() if room.has_zombies)
        total_rooms = sum(len(floor.get_rooms()) for floor in self.building.floors)
        game_over = total_infested == total_rooms

        if game_over:
            logger.info("Juego terminado: todas las habitaciones están infestadas")

        return {
            "turn": self.turn,
            "newly_infested": newly_infested,
            "vacated_rooms": vacated_rooms,
            "total_infested": total_infested,
            "game_over": game_over,
            "new_zombie_generated": new_zombie_generated
        }
    
    def clean_room(self, floor_number, room_number):
        """
        Limpia una habitación, eliminando los zombis en ella.
        
        Args:
            floor_number (int): Número de piso
            room_number (int): Número de habitación
            
        Returns:
            dict: Resultado de la operación
        """
        if not self.building:
            logger.warning("Intento de limpiar habitación sin edificio configurado")
            return {"error": "No hay edificio configurado"}
            
        try:
            room = self.building.get_floor(floor_number).get_room(room_number)
            
            if not room.has_zombies:
                logger.info(f"Intento de limpiar habitación sin zombis: {floor_number}-{room_number}")
                return {"cleaned": False, "message": "No hay zombis en esta habitación"}
                
            room.has_zombies = False
            # No reseteamos el sensor aquí, eso se hace con reset_sensor
            
            logger.info(f"Habitación limpiada: {floor_number}-{room_number}")
            return {"cleaned": True, "message": "Habitación limpiada correctamente"}
            
        except Exception as e:
            logger.error(f"Error al limpiar habitación: {str(e)}")
            return {"error": f"Error al limpiar habitación: {str(e)}"}
    
    def reset_sensor(self, floor_number, room_number):
        """
        Restablece el sensor en una habitación específica.
        
        Args:
            floor_number (int): Número de piso
            room_number (int): Número de habitación
            
        Returns:
            dict: Resultado de la operación
        """
        if not self.building:
            logger.warning("Intento de restablecer sensor sin edificio configurado")
            return {"error": "No hay edificio configurado"}
            
        try:
            room = self.building.get_floor(floor_number).get_room(room_number)
            
            if not room.sensor.is_alert():
                logger.info(f"Intento de restablecer sensor que no está en alerta: {floor_number}-{room_number}")
                return {"reset": False, "message": "El sensor no está en alerta"}
                
            room.sensor.reset()
            
            logger.info(f"Sensor restablecido: {floor_number}-{room_number}")
            return {"reset": True, "message": "Sensor restablecido correctamente"}
            
        except Exception as e:
            logger.error(f"Error al restablecer sensor: {str(e)}")
            return {"error": f"Error al restablecer sensor: {str(e)}"}
    
    def get_building_state(self):
        """
        Obtiene el estado actual del edificio.
        
        Returns:
            dict: Un diccionario con el estado actual del edificio
        """
        if not self.building:
            logger.warning("Intento de obtener estado sin un edificio configurado")
            return {"error": "No hay edificio configurado"}
        
        total_infested = sum(1 for floor in self.building.floors 
                           for room in floor.get_rooms() if room.has_zombies)
        total_rooms = sum(len(floor.get_rooms()) for floor in self.building.floors)
        
        state = {
            "turn": self.turn,
            "floors": len(self.building.floors),
            "rooms_per_floor": len(self.building.floors[0].get_rooms()) if self.building.floors else 0,
            "total_rooms": total_rooms,
            "infested_rooms": total_infested,
            "game_over": total_infested == total_rooms
        }
        
        logger.debug(f"Estado actual del edificio: {state}")
        return state
    
    def is_game_over(self):
        """
        Comprueba si el juego ha terminado (todas las habitaciones infestadas).
        
        Returns:
            bool: True si el juego ha terminado, False en caso contrario
        """
        if not self.building:
            return False
            
        total_infested = sum(1 for floor in self.building.floors 
                           for room in floor.get_rooms() if room.has_zombies)
        total_rooms = sum(len(floor.get_rooms()) for floor in self.building.floors)
        return total_infested == total_rooms 