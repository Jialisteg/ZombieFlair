class Sensor:
    """
    Represents an IoT sensor that can detect zombies in a room.
    The sensor can be in different states: 'normal' or 'alert'.
    """
    
    def __init__(self, id):
        """
        Initialize a new sensor with a unique ID.
        
        Args:
            id: A unique identifier for the sensor
        """
        self.id = id
        self.state = "normal"  # Initial state is normal
    
    def set_alert(self):
        """Set the sensor state to 'alert' when zombies are detected."""
        self.state = "alert"
    
    def reset(self):
        """Reset the sensor state to 'normal'."""
        self.state = "normal"
    
    def is_alert(self):
        """
        Check if the sensor is in alert state.
        
        Returns:
            bool: True if the sensor is in alert state, False otherwise
        """
        return self.state == "alert"
    
    def __str__(self):
        """
        String representation of the sensor.
        
        Returns:
            str: A string showing the sensor ID and state
        """
        return f"Sensor {self.id}: {self.state.upper()}" 