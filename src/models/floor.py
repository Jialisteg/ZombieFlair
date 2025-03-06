from src.models.room import Room

class Floor:
    """
    Representa un piso en un edificio que contiene múltiples habitaciones.
    """
    
    def __init__(self, floor_number, rooms_count):
        """
        Inicializa un nuevo piso con un número específico de habitaciones.
        
        Args:
            floor_number (int): El número de piso
            rooms_count (int): El número de habitaciones en este piso
        """
        self.floor_number = floor_number
        self.rooms = []
        
        # Crear habitaciones para este piso
        for room_number in range(rooms_count):
            self.rooms.append(Room(floor_number, room_number))
        
        # Conectar habitaciones adyacentes en el mismo piso
        self._connect_adjacent_rooms()
    
    def _connect_adjacent_rooms(self):
        """Conecta las habitaciones adyacentes en el mismo piso."""
        for i in range(len(self.rooms)):
            # Conectar con la siguiente habitación (si no es la última habitación)
            if i < len(self.rooms) - 1:
                self.rooms[i].add_adjacent_room(self.rooms[i + 1])
                self.rooms[i + 1].add_adjacent_room(self.rooms[i])
    
    def get_room(self, room_number):
        """
        Obtiene una habitación específica en este piso.
        
        Args:
            room_number (int): El número de habitación a recuperar
            
        Returns:
            Room: La habitación solicitada, o None si no se encuentra
        """
        if 0 <= room_number < len(self.rooms):
            return self.rooms[room_number]
        return None
    
    def get_rooms(self):
        """
        Obtiene todas las habitaciones en este piso.
        
        Returns:
            list: Una lista de todos los objetos Room en este piso
        """
        return self.rooms
    
    def get_rooms_with_zombies(self):
        """
        Obtiene todas las habitaciones en este piso que contienen zombis.
        
        Returns:
            list: Una lista de objetos Room que tienen zombis
        """
        return [room for room in self.rooms if room.has_zombies]
    
    def __str__(self):
        """
        Representación en cadena de texto del piso.
        
        Returns:
            str: Una cadena que muestra el número de piso y un resumen de las habitaciones
        """
        zombie_count = len(self.get_rooms_with_zombies())
        return f"Piso {self.floor_number}: {zombie_count}/{len(self.rooms)} habitaciones infestadas" 