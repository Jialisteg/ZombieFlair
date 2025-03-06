from src.models.sensor import Sensor

class Room:
    """
    Represents a room in a building that may contain zombies.
    Each room has a sensor that detects zombie presence.
    """
    
    def __init__(self, floor_number, room_number):
        """
        Initialize a new room with a floor number and room number.
        
        Args:
            floor_number (int): The floor number where this room is located
            room_number (int): The room number on the floor
        """
        self.floor_number = floor_number
        self.room_number = room_number
        self.has_zombies = False
        self.sensor = Sensor(f"F{floor_number}R{room_number}")
        self.adjacent_rooms = []
    
    def add_adjacent_room(self, room):
        """
        Add an adjacent room that zombies can move to.
        
        Args:
            room (Room): An adjacent room
        """
        if room not in self.adjacent_rooms:
            self.adjacent_rooms.append(room)
    
    def add_zombies(self):
        """Add zombies to the room and trigger the sensor."""
        self.has_zombies = True
        self.sensor.set_alert()
    
    def remove_zombies(self):
        """Remove zombies from the room."""
        self.has_zombies = False
        # Note: We don't reset the sensor automatically
        # as it would stay in alert until manually reset
    
    def reset_sensor(self):
        """Reset the room's sensor to normal state."""
        self.sensor.reset()
    
    def get_adjacent_rooms(self):
        """
        Get all adjacent rooms.
        
        Returns:
            list: A list of adjacent Room objects
        """
        return self.adjacent_rooms
    
    def __str__(self):
        """
        String representation of the room.
        
        Returns:
            str: A string showing the room location and zombie status
        """
        status = "🧟 INFESTED" if self.has_zombies else "✅ CLEAR"
        sensor_status = "🚨 ALERT" if self.sensor.is_alert() else "🟢 NORMAL"
        return f"Room {self.floor_number}-{self.room_number}: {status} | Sensor: {sensor_status}" 