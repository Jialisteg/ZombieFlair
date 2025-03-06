from src.models.floor import Floor

class Building:
    """
    Represents a building with multiple floors and rooms.
    The building is the main container for the zombie simulation.
    """
    
    def __init__(self, floors_count, rooms_per_floor):
        """
        Initialize a new building with a specified number of floors and rooms per floor.
        
        Args:
            floors_count (int): The number of floors in the building
            rooms_per_floor (int): The number of rooms on each floor
        """
        self.floors = []
        
        # Create floors for this building
        for floor_number in range(floors_count):
            self.floors.append(Floor(floor_number, rooms_per_floor))
        
        # Connect rooms between floors (vertical connections)
        self._connect_floors()
    
    def _connect_floors(self):
        """Connect rooms between adjacent floors."""
        for i in range(len(self.floors) - 1):
            current_floor = self.floors[i]
            next_floor = self.floors[i + 1]
            
            # Connect each room to the room directly above/below it
            for room_number in range(len(current_floor.get_rooms())):
                current_room = current_floor.get_room(room_number)
                next_room = next_floor.get_room(room_number)
                
                if current_room and next_room:
                    current_room.add_adjacent_room(next_room)
                    next_room.add_adjacent_room(current_room)
    
    def get_floor(self, floor_number):
        """
        Get a specific floor in the building.
        
        Args:
            floor_number (int): The floor number to retrieve
            
        Returns:
            Floor: The requested floor, or None if not found
        """
        if 0 <= floor_number < len(self.floors):
            return self.floors[floor_number]
        return None
    
    def get_room(self, floor_number, room_number):
        """
        Get a specific room in the building.
        
        Args:
            floor_number (int): The floor number
            room_number (int): The room number
            
        Returns:
            Room: The requested room, or None if not found
        """
        floor = self.get_floor(floor_number)
        if floor:
            return floor.get_room(room_number)
        return None
    
    def get_all_rooms(self):
        """
        Get all rooms in the building.
        
        Returns:
            list: A flat list of all Room objects in the building
        """
        all_rooms = []
        for floor in self.floors:
            all_rooms.extend(floor.get_rooms())
        return all_rooms
    
    def get_all_rooms_with_zombies(self):
        """
        Get all rooms in the building that contain zombies.
        
        Returns:
            list: A list of all Room objects that have zombies
        """
        return [room for room in self.get_all_rooms() if room.has_zombies]
    
    def add_initial_zombie(self, floor_number, room_number):
        """
        Add an initial zombie to a specific room.
        
        Args:
            floor_number (int): The floor number
            room_number (int): The room number
            
        Returns:
            bool: True if zombie was added successfully, False otherwise
        """
        room = self.get_room(floor_number, room_number)
        if room:
            room.add_zombies()
            return True
        return False
    
    def __str__(self):
        """
        String representation of the building.
        
        Returns:
            str: A string showing a summary of the building state
        """
        total_rooms = len(self.get_all_rooms())
        infested_rooms = len(self.get_all_rooms_with_zombies())
        return f"Building: {infested_rooms}/{total_rooms} rooms infested with zombies" 