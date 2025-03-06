class Sensor:
    """
    Representa un sensor IoT que puede detectar zombis en una habitación.
    El sensor puede estar en diferentes estados: 'normal' o 'alerta'.
    """
    
    def __init__(self, id):
        """
        Inicializa un nuevo sensor con un ID único.
        
        Args:
            id: Un identificador único para el sensor
        """
        self.id = id
        self.state = "normal"  # Estado inicial es normal
    
    def set_alert(self):
        """Establece el estado del sensor a 'alerta' cuando se detectan zombis."""
        self.state = "alert"
    
    def reset(self):
        """Restablece el estado del sensor a 'normal'."""
        self.state = "normal"
    
    def is_alert(self):
        """
        Comprueba si el sensor está en estado de alerta.
        
        Returns:
            bool: True si el sensor está en estado de alerta, False en caso contrario
        """
        return self.state == "alert"
    
    def __str__(self):
        """
        Representación en cadena de texto del sensor.
        
        Returns:
            str: Una cadena que muestra el ID del sensor y su estado
        """
        return f"Sensor {self.id}: {self.state.upper()}" 