# Zombie IoT Sensor Simulation

A Python CLI application that simulates a building infested with zombies, using IoT sensors to track the invasion.

## Description

This application simulates a scenario where a building is infested with zombies, and IoT sensors are used to detect their presence. The user can configure the building, add initial zombies, and simulate the spread of the infestation turn by turn.

## Features

- Configure a building with multiple floors and rooms
- Add initial zombies to random rooms
- Simulate zombie movement between adjacent rooms
- Track the state of each room and sensor
- Clean rooms of zombies
- Reset sensors that have been triggered

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/zombie-iot-simulation.git
   cd zombie-iot-simulation
   ```

2. No additional dependencies are required as the application uses only Python standard libraries.

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Follow the on-screen menu to interact with the simulation:
   - Option 1: Setup Building - Configure the number of floors and rooms
   - Option 2: Show Building State - Display the current state of the building
   - Option 3: Advance Simulation - Move zombies to adjacent rooms
   - Option 4: Clean Room - Remove zombies from a specific room
   - Option 5: Reset Sensor - Reset a sensor to normal state
   - Option 6: Exit - Quit the application

## Architecture

The application is structured using object-oriented programming principles:

- **Building**: Manages a collection of floors and provides methods to access rooms
- **Floor**: Contains multiple rooms and handles connections between them
- **Room**: Represents a physical space that may contain zombies and has a sensor
- **Sensor**: Detects zombie presence and can be in "normal" or "alert" state
- **Simulation**: Orchestrates the zombie movement logic and tracks game state
- **ZombieSimulationCLI**: Provides the command-line interface for user interaction

### Zombie Movement Logic

- Zombies spread to adjacent rooms each turn
- Rooms are considered adjacent if they have consecutive room numbers on the same floor
- Rooms are also connected vertically between floors (same room number on different floors)
- When zombies enter a room, the sensor goes into alert state
- The simulation ends when all rooms are infested

## License

This project is licensed under the MIT License - see the LICENSE file for details. 