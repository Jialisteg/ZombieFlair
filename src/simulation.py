import random
from src.models.building import Building
from src.models.staircase import Staircase
from src.models.practicante import Practicante
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
        self.practicante = None
        self.game_over_reason = None
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
            return False, None, None

        # Obtener todas las habitaciones sin zombis
        available_rooms = []
        for floor_idx, floor in enumerate(self.building.floors):
            for room_idx, room in enumerate(floor.get_rooms()):
                if not room.has_zombies:
                    available_rooms.append((floor_idx, room_idx))

        if not available_rooms:
            logger.debug("No hay habitaciones disponibles para generar un nuevo zombi")
            return False, None, None

        # Seleccionar una habitación aleatoria
        floor_idx, room_idx = random.choice(available_rooms)
        room = self.building.get_floor(floor_idx).get_room(room_idx)
        room.add_zombies()  # Usar el método específico de la clase
        
        logger.debug(f"Nuevo zombi generado en piso {floor_idx}, habitación {room_idx}")
        return True, floor_idx, room_idx
    
    def add_random_zombie(self):
        """
        Agrega un nuevo zombi en una habitación aleatoria (invocado por el usuario).
        
        Returns:
            dict: Información sobre el zombi añadido, o error si no se pudo añadir
        """
        success, floor_idx, room_idx = self.generate_random_zombie()
        if success:
            logger.info(f"Usuario agregó un nuevo zombi manualmente en piso {floor_idx}, habitación {room_idx}")
            return {
                "added": True,
                "floor": floor_idx,
                "room": room_idx
            }
        else:
            return {
                "added": False
            }
    
    def use_secret_weapon(self):
        """
        Utiliza el arma secreta para eliminar zombis aleatoriamente.
        Tiene un 50% de probabilidad de eliminar cada zombi.
        
        Returns:
            int: El número de habitaciones limpiadas
        """
        if not self.building:
            return 0
            
        cleaned_count = 0
        zombie_rooms = []
        
        # Identificar todas las habitaciones con zombis
        for floor_idx, floor in enumerate(self.building.floors):
            for room_idx, room in enumerate(floor.get_rooms()):
                if room.has_zombies:
                    zombie_rooms.append((floor_idx, room_idx))
        
        # Para cada habitación con zombis, hay un 50% de probabilidad de eliminarlos
        for floor_idx, room_idx in zombie_rooms:
            if random.random() < 0.5:  # 50% de probabilidad
                room = self.building.get_floor(floor_idx).get_room(room_idx)
                room.has_zombies = False  # Eliminar el zombi pero no resetear el sensor
                cleaned_count += 1
                logger.debug(f"Arma secreta eliminó zombi en piso {floor_idx}, habitación {room_idx}")
        
        logger.info(f"Arma secreta utilizada: {cleaned_count} habitaciones limpiadas")
        return cleaned_count
    
    def setup_building(self, floors_count, rooms_per_floor):
        """
        Configura un nuevo edificio para la simulación.
        
        Args:
            floors_count (int): El número de pisos
            rooms_per_floor (int): El número de habitaciones regulares por piso (sin contar la escalera)
            
        Returns:
            dict: Un diccionario con información sobre el edificio configurado
        """
        self.building = Building(floors_count, rooms_per_floor)
        logger.info(f"Edificio configurado con {floors_count} pisos y {rooms_per_floor} habitaciones regulares por piso")
        
        # Cada piso tiene rooms_per_floor habitaciones regulares + 1 escalera
        rooms_with_stairs_per_floor = rooms_per_floor + 1
        total_rooms = floors_count * rooms_with_stairs_per_floor
        staircases_count = floors_count  # Una escalera por piso
        normal_rooms_count = floors_count * rooms_per_floor  # Total de habitaciones regulares
        
        # Reiniciar variables de estado
        self.practicante = None
        self.game_over_reason = None
        
        return {
            "floors": floors_count,
            "rooms_per_floor": rooms_per_floor,
            "rooms_with_stairs_per_floor": rooms_with_stairs_per_floor,
            "staircases": staircases_count,
            "normal_rooms": normal_rooms_count,
            "total_rooms": total_rooms
        }
    
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
            # Usar el método add_zombies que maneja correctamente tanto habitaciones como escaleras
            room.add_zombies()
            zombies_added.append((floor_idx, room_idx))
            logger.debug(f"Zombi añadido en piso {floor_idx}, habitación {room_idx}")
            
        return zombies_added
    
    def add_practicante(self):
        """
        Añade un practicante (interno) a una habitación aleatoria sin zombis.
        
        Returns:
            dict: Información sobre el practicante añadido, o error si no se pudo añadir
        """
        if not self.building:
            logger.warning("Intento de agregar practicante sin edificio configurado")
            return {"error": "No hay edificio configurado"}
        
        # Si ya hay un practicante, no añadir otro
        if self.practicante:
            logger.warning("Ya existe un practicante en la simulación")
            return {"error": "Ya existe un practicante en la simulación"}
        
        # Obtener todas las habitaciones normales sin zombis
        available_rooms = []
        for floor_idx, floor in enumerate(self.building.floors):
            for room_idx, room in enumerate(floor.get_rooms()):
                # Solo habitaciones regulares (no escaleras) y sin zombis
                if room_idx > 0 and not room.has_zombies:
                    available_rooms.append((floor_idx, room_idx))
        
        if not available_rooms:
            logger.warning("No hay habitaciones disponibles para añadir un practicante")
            return {"error": "No hay habitaciones disponibles para añadir un practicante"}
        
        # Seleccionar una habitación aleatoria
        floor_idx, room_idx = random.choice(available_rooms)
        
        # Crear el practicante
        self.practicante = Practicante(floor_idx, room_idx)
        logger.info(f"Practicante añadido en piso {floor_idx}, habitación {room_idx}")
        
        return {
            "added": True,
            "floor": floor_idx,
            "room": room_idx,
            "message": f"Practicante añadido en piso {floor_idx}, habitación {room_idx}"
        }
    
    def move_practicante(self):
        """
        Mueve el practicante a una habitación adyacente aleatoria sin zombis.
        El practicante intentará evitar habitaciones adyacentes a zombis si es posible.
        
        Returns:
            dict: Información sobre el movimiento, o None si no hay practicante
        """
        if not self.practicante:
            return None
        
        floor_idx, room_idx = self.practicante.get_location()
        current_room = self.building.get_floor(floor_idx).get_room(room_idx)
        
        # Obtener todas las habitaciones adyacentes
        adjacent_rooms = []
        dangerous_rooms = []  # Habitaciones adyacentes a zombis
        
        for adj_room in current_room.get_adjacent_rooms():
            # Encontrar la ubicación (piso, habitación) de esta habitación adyacente
            for adj_floor_idx, adj_floor in enumerate(self.building.floors):
                for adj_room_idx, r in enumerate(adj_floor.get_rooms()):
                    if r is adj_room:
                        location = (adj_floor_idx, adj_room_idx)
                        
                        # Verificar si esta habitación tiene zombis
                        if adj_room.has_zombies:
                            # No incluir habitaciones con zombis
                            continue
                        
                        # Verificar si esta habitación tiene zombis adyacentes
                        has_adjacent_zombies = False
                        for zombie_adj_room in adj_room.get_adjacent_rooms():
                            if zombie_adj_room.has_zombies:
                                has_adjacent_zombies = True
                                break
                        
                        if has_adjacent_zombies:
                            dangerous_rooms.append(location)
                        else:
                            adjacent_rooms.append(location)
                        break
        
        # Verificar si la habitación actual tiene zombis adyacentes
        current_has_adjacent_zombies = False
        for zombie_adj_room in current_room.get_adjacent_rooms():
            if zombie_adj_room.has_zombies:
                current_has_adjacent_zombies = True
                break
        
        # Prioridad: 
        # 1. Habitaciones seguras (sin zombis adyacentes)
        # 2. Habitaciones peligrosas (con zombis adyacentes) pero solo si la actual también es peligrosa
        # 3. Quedarse donde está si no hay opción mejor
        
        if adjacent_rooms:
            # Hay habitaciones seguras disponibles
            new_floor_idx, new_room_idx = random.choice(adjacent_rooms)
            logger.debug(f"Practicante movido de {floor_idx}-{room_idx} a {new_floor_idx}-{new_room_idx} (habitación segura)")
        elif dangerous_rooms and current_has_adjacent_zombies:
            # No hay habitaciones seguras, pero hay opciones menos peligrosas
            new_floor_idx, new_room_idx = random.choice(dangerous_rooms)
            logger.debug(f"Practicante movido de {floor_idx}-{room_idx} a {new_floor_idx}-{new_room_idx} (habitación peligrosa)")
        else:
            # Mejor quedarse donde está
            new_floor_idx, new_room_idx = floor_idx, room_idx
            logger.debug(f"Practicante se queda en {floor_idx}-{room_idx} (no hay rutas más seguras)")
        
        # Si hay que moverse, actualizar posición
        if new_floor_idx != floor_idx or new_room_idx != room_idx:
            self.practicante.move_to(new_floor_idx, new_room_idx)
            return {
                "moved": True,
                "from": (floor_idx, room_idx),
                "to": (new_floor_idx, new_room_idx)
            }
        else:
            return {
                "moved": False,
                "from": (floor_idx, room_idx),
                "to": (floor_idx, room_idx),
                "message": "No hay rutas más seguras disponibles"
            }
    
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
        new_zombie_location = None
        practicante_moved = None

        # Si hay un practicante, moverlo primero
        if self.practicante:
            practicante_moved = self.move_practicante()

        # Para cada piso y habitación con zombis, mover el zombi a UNA habitación adyacente
        zombie_movements = []  # Lista para guardar los movimientos a realizar

        for floor_idx, floor in enumerate(self.building.floors):
            rooms = floor.get_rooms()
            for room_idx, room in enumerate(rooms):
                if room.has_zombies:
                    # Obtener habitaciones adyacentes directamente del objeto habitación
                    adjacent_rooms = room.get_adjacent_rooms()
                    
                    # Filtrar solo las habitaciones adyacentes sin zombis
                    available_adj_rooms = []
                    
                    for adj_room in adjacent_rooms:
                        if not adj_room.has_zombies:
                            # Encontrar los índices para esta habitación adyacente
                            for adj_floor_idx, adj_floor in enumerate(self.building.floors):
                                for adj_room_idx, r in enumerate(adj_floor.get_rooms()):
                                    if r is adj_room:
                                        available_adj_rooms.append((adj_floor_idx, adj_room_idx))
                                        break
                    
                    # Si hay movimientos posibles, elegir uno al azar
                    if available_adj_rooms:
                        target_floor, target_room = random.choice(available_adj_rooms)
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
            target_room.add_zombies()  # Usar el método para activar el sensor si hay
            
            # Registrar el cambio
            vacated_rooms.append((from_floor, from_room))
            newly_infested.append((to_floor, to_room))
            
            logger.debug(f"Zombi movido de piso {from_floor}, habitación {from_room} a piso {to_floor}, habitación {to_room}")
            
            # Verificar si el zombi ha alcanzado al practicante
            if self.practicante and self.practicante.floor_number == to_floor and self.practicante.room_number == to_room:
                self.game_over_reason = "practicante_capturado"
                logger.info(f"¡Juego terminado! Un zombi ha capturado al practicante en piso {to_floor}, habitación {to_room}")

        # Generar un nuevo zombi si está activada la generación
        if self.zombie_generation_enabled:
            success, floor_idx, room_idx = self.generate_random_zombie()
            new_zombie_generated = success
            if success:
                new_zombie_location = (floor_idx, room_idx)

        # Verificar si todas las habitaciones están infestadas
        total_infested = sum(1 for floor in self.building.floors 
                           for room in floor.get_rooms() if room.has_zombies)
        total_rooms = sum(len(floor.get_rooms()) for floor in self.building.floors)
        game_over = total_infested == total_rooms or self.game_over_reason is not None

        return {
            "turn": self.turn,
            "newly_infested": newly_infested,
            "vacated_rooms": vacated_rooms,
            "total_infested": total_infested,
            "game_over": game_over,
            "game_over_reason": self.game_over_reason,
            "new_zombie_generated": new_zombie_generated,
            "new_zombie_location": new_zombie_location,
            "practicante_moved": practicante_moved
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
                
            # Usar el método remove_zombies() para manejar correctamente tanto habitaciones como escaleras
            room.remove_zombies()
            
            # Nombre del tipo de habitación para el mensaje
            room_type = "Escalera" if hasattr(room, 'connected_floors') else "Habitación"
            
            logger.info(f"{room_type} limpiada: {floor_number}-{room_number}")
            return {"cleaned": True, "message": f"{room_type} limpiada correctamente"}
            
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
            
            # Verificar si la habitación es una escalera (no tiene sensor)
            if hasattr(room, 'connected_floors'):
                logger.info(f"Intento de restablecer sensor en una escalera: {floor_number}-{room_number}")
                return {"reset": False, "message": "Las escaleras no tienen sensores"}
            
            if not room.sensor.is_alert():
                logger.info(f"Intento de restablecer sensor que ya está normal: {floor_number}-{room_number}")
                return {"reset": False, "message": "El sensor ya está en estado normal"}
                
            room.reset_sensor()
            
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
            "game_over": total_infested == total_rooms or self.game_over_reason is not None,
            "game_over_reason": self.game_over_reason,
            "practicante": self.practicante.get_location() if self.practicante else None
        }
        
        logger.debug(f"Estado actual del edificio: {state}")
        return state
    
    def is_game_over(self):
        """
        Comprueba si el juego ha terminado (todas las habitaciones infestadas o el practicante ha sido capturado).
        
        Returns:
            bool: True si el juego ha terminado, False en caso contrario
        """
        if not self.building:
            return False
            
        if self.game_over_reason is not None:
            return True
            
        total_infested = sum(1 for floor in self.building.floors 
                           for room in floor.get_rooms() if room.has_zombies)
        total_rooms = sum(len(floor.get_rooms()) for floor in self.building.floors)
        return total_infested == total_rooms 