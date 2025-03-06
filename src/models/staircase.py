from src.models.room import Room

class Staircase(Room):
    """
    Representa una escalera en el edificio que permite a los zombis moverse entre pisos.
    Hereda de Room pero no tiene sensor y posee un ícono diferente.
    """
    
    def __init__(self, floor_number, room_number=0):
        """
        Inicializa una nueva escalera.
        
        Args:
            floor_number (int): El número de piso donde se encuentra esta escalera
            room_number (int): El número de habitación de la escalera (por defecto 0)
        """
        super().__init__(floor_number, room_number)
        # Las escaleras no tienen sensores, así que lo eliminamos
        self.sensor = None
        # Lista de pisos conectados a esta escalera
        self.connected_floors = []
        
    def add_connected_floor(self, floor):
        """
        Conecta esta escalera con un piso adyacente.
        
        Args:
            floor (Floor): Un piso adyacente al que se puede acceder desde esta escalera
        """
        if floor not in self.connected_floors:
            self.connected_floors.append(floor)
    
    def get_connected_floors(self):
        """
        Obtiene todos los pisos conectados a esta escalera.
        
        Returns:
            list: Una lista de objetos Floor conectados
        """
        return self.connected_floors
    
    def add_zombies(self):
        """Añade zombis a la escalera. Sobrescribe el método para evitar problemas con el sensor."""
        self.has_zombies = True
        # No hacemos nada con el sensor ya que no existe
    
    def reset_sensor(self):
        """Sobrescribe el método para que no haga nada, ya que no hay sensor."""
        pass
        
    def __str__(self):
        """
        Representación en cadena de texto de la escalera.
        
        Returns:
            str: Una cadena que muestra la ubicación de la escalera y el estado de los zombis
        """
        status = "🧟 INFESTADA" if self.has_zombies else "✅ DESPEJADA"
        return f"Escalera {self.floor_number}-{self.room_number}: {status} | 🪜 ESCALERA" 