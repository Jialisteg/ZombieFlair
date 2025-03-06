import random
from src.models.building import Building

class Simulation:
    """
    Manages the zombie simulation, including zombie movement and game state.
    """
    
    def __init__(self):
        """Initialize a new simulation with no building."""
        self.building = None
        self.turn_count = 0
        self.game_over = False
    
    def setup_building(self, floors_count, rooms_per_floor):
        """
        Set up a new building for the simulation.
        
        Args:
            floors_count (int): The number of floors in the building
            rooms_per_floor (int): The number of rooms on each floor
        """
        self.building = Building(floors_count, rooms_per_floor)
        self.turn_count = 0
        self.game_over = False
        return self.building
    
    def add_initial_zombies(self, count=1):
        """
        Add initial zombies to random rooms in the building.
        
        Args:
            count (int): The number of initial zombies to add
            
        Returns:
            list: The rooms where zombies were added
        """
        if not self.building:
            return []
        
        all_rooms = self.building.get_all_rooms()
        if not all_rooms:
            return []
        
        # Select random rooms for initial zombies
        zombie_rooms = []
        for _ in range(min(count, len(all_rooms))):
            # Choose a room that doesn't already have zombies
            available_rooms = [room for room in all_rooms if not room.has_zombies]
            if not available_rooms:
                break
                
            room = random.choice(available_rooms)
            room.add_zombies()
            zombie_rooms.append(room)
        
        return zombie_rooms
    
    def advance_turn(self):
        """
        Advance the simulation by one turn, moving zombies to adjacent rooms.
        
        Returns:
            dict: Statistics about the turn, including new infestations
        """
        if not self.building or self.game_over:
            return {"error": "No building configured or game is over"}
        
        self.turn_count += 1
        
        # Get all rooms with zombies before movement
        rooms_with_zombies = self.building.get_all_rooms_with_zombies()
        newly_infested_rooms = []
        
        # For each room with zombies, spread to adjacent rooms
        for room in rooms_with_zombies:
            adjacent_rooms = room.get_adjacent_rooms()
            
            for adj_room in adjacent_rooms:
                if not adj_room.has_zombies:
                    adj_room.add_zombies()
                    newly_infested_rooms.append(adj_room)
        
        # Check if all rooms are infested (game over condition)
        all_rooms = self.building.get_all_rooms()
        if all(room.has_zombies for room in all_rooms):
            self.game_over = True
        
        return {
            "turn": self.turn_count,
            "newly_infested": newly_infested_rooms,
            "total_infested": len(self.building.get_all_rooms_with_zombies()),
            "game_over": self.game_over
        }
    
    def clean_room(self, floor_number, room_number):
        """
        Clean zombies from a specific room.
        
        Args:
            floor_number (int): The floor number
            room_number (int): The room number
            
        Returns:
            bool: True if room was cleaned successfully, False otherwise
        """
        room = self.building.get_room(floor_number, room_number)
        if room and room.has_zombies:
            room.remove_zombies()
            return True
        return False
    
    def reset_sensor(self, floor_number, room_number):
        """
        Reset the sensor in a specific room.
        
        Args:
            floor_number (int): The floor number
            room_number (int): The room number
            
        Returns:
            bool: True if sensor was reset successfully, False otherwise
        """
        room = self.building.get_room(floor_number, room_number)
        if room:
            room.reset_sensor()
            return True
        return False
    
    def get_building_state(self):
        """
        Get the current state of the building.
        
        Returns:
            dict: A dictionary with the current building state
        """
        if not self.building:
            return {"error": "No building configured"}
        
        return {
            "turn": self.turn_count,
            "floors": len(self.building.floors),
            "rooms_per_floor": len(self.building.floors[0].get_rooms()) if self.building.floors else 0,
            "total_rooms": len(self.building.get_all_rooms()),
            "infested_rooms": len(self.building.get_all_rooms_with_zombies()),
            "game_over": self.game_over
        }
    
    def is_game_over(self):
        """
        Check if the game is over (all rooms infested).
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.game_over 