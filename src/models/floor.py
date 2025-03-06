from src.models.room import Room

class Floor:
    """
    Represents a floor in a building that contains multiple rooms.
    """
    
    def __init__(self, floor_number, rooms_count):
        """
        Initialize a new floor with a specified number of rooms.
        
        Args:
            floor_number (int): The floor number
            rooms_count (int): The number of rooms on this floor
        """
        self.floor_number = floor_number
        self.rooms = []
        
        # Create rooms for this floor
        for room_number in range(rooms_count):
            self.rooms.append(Room(floor_number, room_number))
        
        # Connect adjacent rooms on the same floor
        self._connect_adjacent_rooms()
    
    def _connect_adjacent_rooms(self):
        """Connect adjacent rooms on the same floor."""
        for i in range(len(self.rooms)):
            # Connect to the next room (if not the last room)
            if i < len(self.rooms) - 1:
                self.rooms[i].add_adjacent_room(self.rooms[i + 1])
                self.rooms[i + 1].add_adjacent_room(self.rooms[i])
    
    def get_room(self, room_number):
        """
        Get a specific room on this floor.
        
        Args:
            room_number (int): The room number to retrieve
            
        Returns:
            Room: The requested room, or None if not found
        """
        if 0 <= room_number < len(self.rooms):
            return self.rooms[room_number]
        return None
    
    def get_rooms(self):
        """
        Get all rooms on this floor.
        
        Returns:
            list: A list of all Room objects on this floor
        """
        return self.rooms
    
    def get_rooms_with_zombies(self):
        """
        Get all rooms on this floor that contain zombies.
        
        Returns:
            list: A list of Room objects that have zombies
        """
        return [room for room in self.rooms if room.has_zombies]
    
    def __str__(self):
        """
        String representation of the floor.
        
        Returns:
            str: A string showing the floor number and a summary of rooms
        """
        zombie_count = len(self.get_rooms_with_zombies())
        return f"Floor {self.floor_number}: {zombie_count}/{len(self.rooms)} rooms infested" 