from src.models.sensor import Sensor

class Room:
    """
    Representa una habitación en un edificio que puede contener zombis.
    Cada habitación tiene un sensor que detecta la presencia de zombis.
    """
    
    def __init__(self, floor_number, room_number):
        """
        Inicializa una nueva habitación con un número de piso y número de habitación.
        
        Args:
            floor_number (int): El número de piso donde se encuentra esta habitación
            room_number (int): El número de habitación en el piso
        """
        self.floor_number = floor_number
        self.room_number = room_number
        self.has_zombies = False
        self.sensor = Sensor(f"P{floor_number}H{room_number}")
        self.adjacent_rooms = []
    
    def add_adjacent_room(self, room):
        """
        Añade una habitación adyacente a la que los zombis pueden moverse.
        
        Args:
            room (Room): Una habitación adyacente
        """
        if room not in self.adjacent_rooms:
            self.adjacent_rooms.append(room)
    
    def add_zombies(self):
        """Añade zombis a la habitación y activa el sensor."""
        self.has_zombies = True
        self.sensor.set_alert()
    
    def remove_zombies(self):
        """Elimina los zombis de la habitación."""
        self.has_zombies = False
        # Nota: No restablecemos el sensor automáticamente
        # ya que permanecería en alerta hasta que se restablezca manualmente
    
    def reset_sensor(self):
        """Restablece el sensor de la habitación al estado normal."""
        self.sensor.reset()
    
    def get_adjacent_rooms(self):
        """
        Obtiene todas las habitaciones adyacentes.
        
        Returns:
            list: Una lista de objetos Room adyacentes
        """
        return self.adjacent_rooms
    
    def __str__(self):
        """
        Representación en cadena de texto de la habitación.
        
        Returns:
            str: Una cadena que muestra la ubicación de la habitación y el estado de los zombis
        """
        status = "🧟 INFESTADA" if self.has_zombies else "✅ DESPEJADA"
        sensor_status = "🚨 ALERTA" if self.sensor.is_alert() else "🟢 NORMAL"
        return f"Habitación {self.floor_number}-{self.room_number}: {status} | Sensor: {sensor_status}" 