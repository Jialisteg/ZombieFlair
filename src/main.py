#!/usr/bin/env python3
import os
import sys
import time
from src.simulation import Simulation

class ZombieSimulationCLI:
    """
    Command-line interface for the Zombie IoT Sensor Simulation.
    """
    
    def __init__(self):
        """Initialize the CLI with a new simulation."""
        self.simulation = Simulation()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        self.clear_screen()
        print("=" * 80)
        print("🧟 ZOMBIE IOT SENSOR SIMULATION 🧟".center(80))
        print("=" * 80)
        print()
    
    def print_building_state(self):
        """Print the current state of the building."""
        if not self.simulation.building:
            print("No building configured yet. Use option 1 to set up a building.")
            return
        
        state = self.simulation.get_building_state()
        
        print(f"\nTurn: {state['turn']}")
        print(f"Building Status: {state['infested_rooms']}/{state['total_rooms']} rooms infested")
        print()
        
        # Print each floor and its rooms
        for floor_idx in range(len(self.simulation.building.floors)):
            floor = self.simulation.building.get_floor(floor_idx)
            print(f"Floor {floor_idx}:")
            
            # Print rooms in a grid format
            rooms_per_row = 5
            rooms = floor.get_rooms()
            
            for i in range(0, len(rooms), rooms_per_row):
                row_rooms = rooms[i:i+rooms_per_row]
                
                # Print room numbers
                print("  ", end="")
                for j, room in enumerate(row_rooms):
                    print(f"Room {room.room_number}".ljust(15), end="")
                print()
                
                # Print zombie status
                print("  ", end="")
                for room in row_rooms:
                    status = "🧟" if room.has_zombies else "  "
                    print(f"[{status}]".ljust(15), end="")
                print()
                
                # Print sensor status
                print("  ", end="")
                for room in row_rooms:
                    sensor = "🚨" if room.sensor.is_alert() else "🟢"
                    print(f"({sensor})".ljust(15), end="")
                print("\n")
            
            print()
        
        if self.simulation.is_game_over():
            print("\n🚨 GAME OVER: All rooms have been infested with zombies! 🚨\n")
    
    def setup_building(self):
        """Set up a new building for the simulation."""
        self.print_header()
        print("BUILDING SETUP")
        print("-" * 80)
        
        try:
            floors_count = int(input("Enter number of floors: "))
            if floors_count <= 0:
                print("Number of floors must be positive.")
                input("Press Enter to continue...")
                return
            
            rooms_per_floor = int(input("Enter number of rooms per floor: "))
            if rooms_per_floor <= 0:
                print("Number of rooms must be positive.")
                input("Press Enter to continue...")
                return
            
            self.simulation.setup_building(floors_count, rooms_per_floor)
            
            # Add initial zombies
            zombie_count = int(input("Enter number of initial zombies: "))
            if zombie_count <= 0:
                print("Number of zombies must be positive.")
                input("Press Enter to continue...")
                return
            
            self.simulation.add_initial_zombies(zombie_count)
            
            print("\nBuilding setup complete!")
            input("Press Enter to continue...")
            
        except ValueError:
            print("Please enter valid numbers.")
            input("Press Enter to continue...")
    
    def advance_simulation(self):
        """Advance the simulation by one turn."""
        if not self.simulation.building:
            self.print_header()
            print("No building configured yet. Use option 1 to set up a building.")
            input("Press Enter to continue...")
            return
        
        result = self.simulation.advance_turn()
        
        self.print_header()
        self.print_building_state()
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"\nTurn {result['turn']} completed.")
            print(f"Newly infested rooms: {len(result['newly_infested'])}")
            print(f"Total infested rooms: {result['total_infested']}")
            
            if result['game_over']:
                print("\n🚨 GAME OVER: All rooms have been infested with zombies! 🚨")
        
        input("\nPress Enter to continue...")
    
    def clean_room(self):
        """Clean zombies from a specific room."""
        if not self.simulation.building:
            self.print_header()
            print("No building configured yet. Use option 1 to set up a building.")
            input("Press Enter to continue...")
            return
        
        self.print_header()
        self.print_building_state()
        
        print("\nCLEAN ROOM")
        print("-" * 80)
        
        try:
            floor_number = int(input("Enter floor number: "))
            room_number = int(input("Enter room number: "))
            
            if self.simulation.clean_room(floor_number, room_number):
                print(f"\nRoom {floor_number}-{room_number} has been cleaned of zombies.")
            else:
                print(f"\nFailed to clean room {floor_number}-{room_number}. Check if it exists and has zombies.")
            
            input("\nPress Enter to continue...")
            
        except ValueError:
            print("Please enter valid numbers.")
            input("Press Enter to continue...")
    
    def reset_sensor(self):
        """Reset a sensor in a specific room."""
        if not self.simulation.building:
            self.print_header()
            print("No building configured yet. Use option 1 to set up a building.")
            input("Press Enter to continue...")
            return
        
        self.print_header()
        self.print_building_state()
        
        print("\nRESET SENSOR")
        print("-" * 80)
        
        try:
            floor_number = int(input("Enter floor number: "))
            room_number = int(input("Enter room number: "))
            
            if self.simulation.reset_sensor(floor_number, room_number):
                print(f"\nSensor in room {floor_number}-{room_number} has been reset.")
            else:
                print(f"\nFailed to reset sensor in room {floor_number}-{room_number}. Check if it exists.")
            
            input("\nPress Enter to continue...")
            
        except ValueError:
            print("Please enter valid numbers.")
            input("Press Enter to continue...")
    
    def show_menu(self):
        """Show the main menu and get user input."""
        self.print_header()
        
        if self.simulation.building:
            self.print_building_state()
        
        print("\nMAIN MENU")
        print("-" * 80)
        print("1. Setup Building")
        print("2. Show Building State")
        print("3. Advance Simulation (Next Turn)")
        print("4. Clean Room (Remove Zombies)")
        print("5. Reset Sensor")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            self.setup_building()
        elif choice == "2":
            self.print_header()
            self.print_building_state()
            input("\nPress Enter to continue...")
        elif choice == "3":
            self.advance_simulation()
        elif choice == "4":
            self.clean_room()
        elif choice == "5":
            self.reset_sensor()
        elif choice == "6":
            self.running = False
            print("\nThank you for using the Zombie IoT Sensor Simulation!")
            time.sleep(1)
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
    
    def run(self):
        """Run the main application loop."""
        while self.running:
            self.show_menu()


if __name__ == "__main__":
    app = ZombieSimulationCLI()
    app.run() 