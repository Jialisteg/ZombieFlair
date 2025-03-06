import random
from src.models.building import Building
from src import logger

class Simulation:
    """
    Gestiona la simulación de zombis, incluyendo el movimiento de zombis y el estado del juego.
    """
    
    def __init__(self):
        """Inicializa una nueva simulación sin edificio."""
        self.building = None
        self.turn_count = 0
        self.game_over = False
        logger.debug("Simulación inicializada")
    
    def setup_building(self, floors_count, rooms_per_floor):
        """
        Configura un nuevo edificio para la simulación.
        
        Args:
            floors_count (int): El número de pisos en el edificio
            rooms_per_floor (int): El número de habitaciones en cada piso
        """
        logger.info(f"Configurando edificio: {floors_count} pisos, {rooms_per_floor} habitaciones por piso")
        self.building = Building(floors_count, rooms_per_floor)
        self.turn_count = 0
        self.game_over = False
        logger.debug("Edificio configurado correctamente")
        return self.building
    
    def add_initial_zombies(self, count=1):
        """
        Añade zombis iniciales a habitaciones aleatorias en el edificio.
        
        Args:
            count (int): El número de zombis iniciales a añadir
            
        Returns:
            list: Las habitaciones donde se añadieron zombis
        """
        if not self.building:
            logger.warning("Intento de añadir zombis sin un edificio configurado")
            return []
        
        logger.info(f"Añadiendo {count} zombis iniciales")
        all_rooms = self.building.get_all_rooms()
        if not all_rooms:
            logger.warning("No hay habitaciones disponibles en el edificio")
            return []
        
        # Seleccionar habitaciones aleatorias para zombis iniciales
        zombie_rooms = []
        for _ in range(min(count, len(all_rooms))):
            # Elegir una habitación que no tenga ya zombis
            available_rooms = [room for room in all_rooms if not room.has_zombies]
            if not available_rooms:
                logger.debug("No hay más habitaciones disponibles para añadir zombis")
                break
                
            room = random.choice(available_rooms)
            room.add_zombies()
            zombie_rooms.append(room)
            logger.debug(f"Zombi añadido a la habitación {room.floor_number}-{room.room_number}")
        
        logger.info(f"Zombis iniciales añadidos: {len(zombie_rooms)} de {count} solicitados")
        return zombie_rooms
    
    def advance_turn(self):
        """
        Avanza la simulación en un turno, moviendo zombis a habitaciones adyacentes.
        
        Returns:
            dict: Estadísticas sobre el turno, incluyendo nuevas infestaciones
        """
        if not self.building or self.game_over:
            logger.warning("Intento de avanzar turno sin edificio configurado o juego terminado")
            return {"error": "No hay edificio configurado o el juego ha terminado"}
        
        self.turn_count += 1
        logger.info(f"Avanzando al turno {self.turn_count}")
        
        # Obtener todas las habitaciones con zombis antes del movimiento
        rooms_with_zombies = self.building.get_all_rooms_with_zombies()
        logger.debug(f"Habitaciones con zombis antes del movimiento: {len(rooms_with_zombies)}")
        newly_infested_rooms = []
        
        # Para cada habitación con zombis, extender a habitaciones adyacentes
        for room in rooms_with_zombies:
            adjacent_rooms = room.get_adjacent_rooms()
            logger.debug(f"Habitación {room.floor_number}-{room.room_number} tiene {len(adjacent_rooms)} habitaciones adyacentes")
            
            for adj_room in adjacent_rooms:
                if not adj_room.has_zombies:
                    adj_room.add_zombies()
                    newly_infested_rooms.append(adj_room)
                    logger.debug(f"Nueva infestación en habitación {adj_room.floor_number}-{adj_room.room_number}")
        
        # Comprobar si todas las habitaciones están infestadas (condición de fin de juego)
        all_rooms = self.building.get_all_rooms()
        if all(room.has_zombies for room in all_rooms):
            self.game_over = True
            logger.info("¡JUEGO TERMINADO! Todas las habitaciones han sido infestadas")
        
        total_infested = len(self.building.get_all_rooms_with_zombies())
        logger.info(f"Turno {self.turn_count} completado: {len(newly_infested_rooms)} nuevas infestaciones, {total_infested} total")
        
        return {
            "turn": self.turn_count,
            "newly_infested": newly_infested_rooms,
            "total_infested": total_infested,
            "game_over": self.game_over
        }
    
    def clean_room(self, floor_number, room_number):
        """
        Limpia los zombis de una habitación específica.
        
        Args:
            floor_number (int): El número de piso
            room_number (int): El número de habitación
            
        Returns:
            bool: True si la habitación se limpió correctamente, False en caso contrario
        """
        logger.info(f"Intentando limpiar habitación {floor_number}-{room_number}")
        room = self.building.get_room(floor_number, room_number)
        if room and room.has_zombies:
            room.remove_zombies()
            logger.info(f"Habitación {floor_number}-{room_number} limpiada con éxito")
            return True
        
        if not room:
            logger.warning(f"No se pudo encontrar la habitación {floor_number}-{room_number}")
        elif not room.has_zombies:
            logger.warning(f"La habitación {floor_number}-{room_number} no tiene zombis para limpiar")
        
        return False
    
    def reset_sensor(self, floor_number, room_number):
        """
        Restablece el sensor en una habitación específica.
        
        Args:
            floor_number (int): El número de piso
            room_number (int): El número de habitación
            
        Returns:
            bool: True si el sensor se restableció correctamente, False en caso contrario
        """
        logger.info(f"Intentando restablecer sensor en habitación {floor_number}-{room_number}")
        room = self.building.get_room(floor_number, room_number)
        if room:
            room.reset_sensor()
            logger.info(f"Sensor en habitación {floor_number}-{room_number} restablecido con éxito")
            return True
        
        logger.warning(f"No se pudo encontrar la habitación {floor_number}-{room_number}")
        return False
    
    def get_building_state(self):
        """
        Obtiene el estado actual del edificio.
        
        Returns:
            dict: Un diccionario con el estado actual del edificio
        """
        if not self.building:
            logger.warning("Intento de obtener estado sin un edificio configurado")
            return {"error": "No hay edificio configurado"}
        
        state = {
            "turn": self.turn_count,
            "floors": len(self.building.floors),
            "rooms_per_floor": len(self.building.floors[0].get_rooms()) if self.building.floors else 0,
            "total_rooms": len(self.building.get_all_rooms()),
            "infested_rooms": len(self.building.get_all_rooms_with_zombies()),
            "game_over": self.game_over
        }
        
        logger.debug(f"Estado actual del edificio: {state}")
        return state
    
    def is_game_over(self):
        """
        Comprueba si el juego ha terminado (todas las habitaciones infestadas).
        
        Returns:
            bool: True si el juego ha terminado, False en caso contrario
        """
        return self.game_over 