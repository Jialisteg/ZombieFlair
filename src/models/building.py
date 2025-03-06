from src.models.floor import Floor

class Building:
    """
    Representa un edificio con múltiples pisos y habitaciones.
    El edificio es el contenedor principal para la simulación de zombis.
    """
    
    def __init__(self, floors_count, rooms_per_floor):
        """
        Inicializa un nuevo edificio con un número específico de pisos y habitaciones por piso.
        
        Args:
            floors_count (int): El número de pisos en el edificio
            rooms_per_floor (int): El número de habitaciones en cada piso
        """
        self.floors = []
        
        # Crear pisos para este edificio
        for floor_number in range(floors_count):
            self.floors.append(Floor(floor_number, rooms_per_floor))
        
        # Conectar habitaciones entre pisos (conexiones verticales)
        self._connect_floors()
    
    def _connect_floors(self):
        """Conecta habitaciones entre pisos adyacentes."""
        for i in range(len(self.floors) - 1):
            current_floor = self.floors[i]
            next_floor = self.floors[i + 1]
            
            # Conectar cada habitación a la habitación directamente arriba/abajo
            for room_number in range(len(current_floor.get_rooms())):
                current_room = current_floor.get_room(room_number)
                next_room = next_floor.get_room(room_number)
                
                if current_room and next_room:
                    current_room.add_adjacent_room(next_room)
                    next_room.add_adjacent_room(current_room)
    
    def get_floor(self, floor_number):
        """
        Obtiene un piso específico en el edificio.
        
        Args:
            floor_number (int): El número de piso a recuperar
            
        Returns:
            Floor: El piso solicitado, o None si no se encuentra
        """
        if 0 <= floor_number < len(self.floors):
            return self.floors[floor_number]
        return None
    
    def get_room(self, floor_number, room_number):
        """
        Obtiene una habitación específica en el edificio.
        
        Args:
            floor_number (int): El número de piso
            room_number (int): El número de habitación
            
        Returns:
            Room: La habitación solicitada, o None si no se encuentra
        """
        floor = self.get_floor(floor_number)
        if floor:
            return floor.get_room(room_number)
        return None
    
    def get_all_rooms(self):
        """
        Obtiene todas las habitaciones en el edificio.
        
        Returns:
            list: Una lista plana de todos los objetos Room en el edificio
        """
        all_rooms = []
        for floor in self.floors:
            all_rooms.extend(floor.get_rooms())
        return all_rooms
    
    def get_all_rooms_with_zombies(self):
        """
        Obtiene todas las habitaciones en el edificio que contienen zombis.
        
        Returns:
            list: Una lista de todos los objetos Room que tienen zombis
        """
        return [room for room in self.get_all_rooms() if room.has_zombies]
    
    def add_initial_zombie(self, floor_number, room_number):
        """
        Añade un zombi inicial a una habitación específica.
        
        Args:
            floor_number (int): El número de piso
            room_number (int): El número de habitación
            
        Returns:
            bool: True si el zombi se añadió correctamente, False en caso contrario
        """
        room = self.get_room(floor_number, room_number)
        if room:
            room.add_zombies()
            return True
        return False
    
    def __str__(self):
        """
        Representación en cadena de texto del edificio.
        
        Returns:
            str: Una cadena que muestra un resumen del estado del edificio
        """
        total_rooms = len(self.get_all_rooms())
        infested_rooms = len(self.get_all_rooms_with_zombies())
        return f"Edificio: {infested_rooms}/{total_rooms} habitaciones infestadas con zombis" 