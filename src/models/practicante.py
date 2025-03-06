"""
Módulo que define la clase Practicante (interno) para la simulación.
"""

class Practicante:
    """
    Representa a un Practicante (Interno) que se mueve por el edificio.
    El practicante debe evitar a los zombis, ya que si un zombi llega a la misma 
    habitación que el practicante, el juego termina.
    A diferencia de los zombis, el practicante no activa los sensores al entrar en una habitación.
    """
    
    def __init__(self, floor_number, room_number):
        """
        Inicializa un nuevo practicante en una habitación específica.
        
        Args:
            floor_number (int): Número de piso donde se encuentra el practicante
            room_number (int): Número de habitación donde se encuentra el practicante
        """
        self.floor_number = floor_number
        self.room_number = room_number
        self.icon = "🚶"
    
    def move_to(self, floor_number, room_number):
        """
        Mueve el practicante a una nueva habitación.
        
        Args:
            floor_number (int): Número de piso de destino
            room_number (int): Número de habitación de destino
        """
        self.floor_number = floor_number
        self.room_number = room_number
    
    def get_location(self):
        """
        Obtiene la ubicación actual del practicante.
        
        Returns:
            tuple: (floor_number, room_number)
        """
        return (self.floor_number, self.room_number)
    
    def __str__(self):
        """
        Representación en texto del practicante.
        """
        return f"Practicante en piso {self.floor_number}, habitación {self.room_number}" 