from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from src.simulation import Simulation
import threading
import time
import logging
import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zombie Building Simulation API",
    description="API for controlling and visualizing a zombie-infested building simulation",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global simulation instance
simulation = Simulation()
simulation_lock = threading.Lock()
simulation_running = False
simulation_thread = None

# Pydantic models for request and response validation
class BuildingConfig(BaseModel):
    floors: int = Field(3, ge=1, description="Number of floors in the building")
    roomsPerFloor: int = Field(5, ge=1, description="Number of rooms per floor")
    initialZombies: int = Field(1, ge=0, description="Initial number of zombies")

class RoomAction(BaseModel):
    floor: int = Field(..., ge=0, description="Floor index")
    room: int = Field(..., ge=0, description="Room index")

class AutoRunConfig(BaseModel):
    run: bool = Field(False, description="Whether to enable auto-running")

# Background task for auto-running the simulation
def run_simulation_task():
    """Background task function to advance simulation automatically"""
    global simulation_running
    while simulation_running:
        with simulation_lock:
            if simulation.building and not simulation.is_game_over():
                simulation.advance_turn()
        time.sleep(1)  # Wait for 1 second between turns

def get_simulation_lock():
    """Dependency to provide the simulation lock"""
    return simulation_lock

@app.get("/api/simulation/state", response_model=Dict[str, Any], tags=["Simulation"])
async def get_simulation_state(lock: threading.Lock = Depends(get_simulation_lock)):
    """Get the current state of the simulation"""
    with lock:
        if not simulation.building:
            raise HTTPException(status_code=404, detail="No building configured")
        
        state = simulation.get_building_state()
        
        # Add additional information for the front-end
        state['game_over'] = simulation.is_game_over()
        state['game_over_reason'] = simulation.game_over_reason
        state['zombie_generation_enabled'] = simulation.zombie_generation_enabled
        
        # Add practicante information if exists
        if simulation.practicante:
            state['practicante'] = {
                'floor': simulation.practicante.floor_number,
                'room': simulation.practicante.room_number
            }
        else:
            state['practicante'] = None
        
        # Add building structure
        building_data = []
        for floor_idx, floor in enumerate(simulation.building.floors):
            floor_data = []
            for room_idx, room in enumerate(floor.get_rooms()):
                room_data = {
                    'floor': floor_idx,
                    'room': room.room_number,
                    'has_zombies': room.has_zombies,
                    'is_staircase': hasattr(room, 'connected_floors'),
                }
                
                # Add sensor data for regular rooms
                if not room_data['is_staircase']:
                    room_data['sensor_alert'] = room.sensor.is_alert()
                
                floor_data.append(room_data)
            building_data.append(floor_data)
        
        state['building'] = building_data
        
        return state

@app.post("/api/simulation/setup", response_model=Dict[str, Any], tags=["Simulation"])
async def setup_simulation(config: BuildingConfig, lock: threading.Lock = Depends(get_simulation_lock)):
    """Setup a new building for the simulation"""
    with lock:
        result = simulation.setup_building(config.floors, config.roomsPerFloor)
        zombies_added = simulation.add_initial_zombies(config.initialZombies)
        
        return {
            "success": True,
            "building": result,
            "zombies_added": zombies_added
        }

@app.post("/api/simulation/advance", response_model=Dict[str, Any], tags=["Simulation"])
async def advance_simulation(lock: threading.Lock = Depends(get_simulation_lock)):
    """Advance the simulation by one turn"""
    with lock:
        if not simulation.building:
            raise HTTPException(status_code=404, detail="No building configured")
        
        result = simulation.advance_turn()
        return result

@app.post("/api/simulation/add-zombie", response_model=Dict[str, Any], tags=["Zombies"])
async def add_zombie(lock: threading.Lock = Depends(get_simulation_lock)):
    """Add a zombie to a random room"""
    with lock:
        if not simulation.building:
            raise HTTPException(status_code=404, detail="No building configured")
        
        result = simulation.add_random_zombie()
        return result

@app.post("/api/simulation/add-practicante", response_model=Dict[str, Any], tags=["Practicante"])
async def add_practicante(lock: threading.Lock = Depends(get_simulation_lock)):
    """Add a practicante to a random room without zombies"""
    with lock:
        if not simulation.building:
            raise HTTPException(status_code=404, detail="No building configured")
        
        result = simulation.add_practicante()
        return result

@app.post("/api/simulation/clean-room", response_model=Dict[str, Any], tags=["Rooms"])
async def clean_room(room_data: RoomAction, lock: threading.Lock = Depends(get_simulation_lock)):
    """Clean a room (remove zombies)"""
    with lock:
        if not simulation.building:
            raise HTTPException(status_code=404, detail="No building configured")
        
        result = simulation.clean_room(room_data.floor, room_data.room)
        return result

@app.post("/api/simulation/reset-sensor", response_model=Dict[str, Any], tags=["Rooms"])
async def reset_sensor(room_data: RoomAction, lock: threading.Lock = Depends(get_simulation_lock)):
    """Reset a sensor in a room"""
    with lock:
        if not simulation.building:
            raise HTTPException(status_code=404, detail="No building configured")
        
        result = simulation.reset_sensor(room_data.floor, room_data.room)
        return result

@app.post("/api/simulation/toggle-zombie-generation", response_model=Dict[str, Any], tags=["Zombies"])
async def toggle_zombie_generation(lock: threading.Lock = Depends(get_simulation_lock)):
    """Toggle automatic zombie generation"""
    with lock:
        enabled = simulation.toggle_zombie_generation()
        return {"zombie_generation_enabled": enabled}

@app.post("/api/simulation/use-secret-weapon", response_model=Dict[str, Any], tags=["Weapons"])
async def use_secret_weapon(lock: threading.Lock = Depends(get_simulation_lock)):
    """Use the secret weapon to clean multiple rooms"""
    with lock:
        if not simulation.building:
            raise HTTPException(status_code=404, detail="No building configured")
        
        cleaned_count = simulation.use_secret_weapon()
        return {"cleaned_count": cleaned_count}

@app.post("/api/simulation/auto-run", response_model=Dict[str, bool], tags=["Simulation"])
async def toggle_auto_run(config: AutoRunConfig, background_tasks: BackgroundTasks, lock: threading.Lock = Depends(get_simulation_lock)):
    """Toggle automatic simulation running"""
    global simulation_running, simulation_thread
    
    with lock:
        should_run = config.run
        
        if should_run and not simulation_running:
            # Start auto-running
            simulation_running = True
            background_tasks.add_task(run_simulation_task)
            return {"auto_running": True}
        elif not should_run and simulation_running:
            # Stop auto-running
            simulation_running = False
            return {"auto_running": False}
        
        # Return current state
        return {"auto_running": simulation_running}

@app.post("/api/simulation/reset", response_model=Dict[str, bool], tags=["Simulation"])
async def reset_simulation(lock: threading.Lock = Depends(get_simulation_lock)):
    """Reset the simulation"""
    global simulation
    
    with lock:
        # Create a new simulation instance
        simulation = Simulation()
        return {"success": True}

# Swagger UI will be available at /docs
# ReDoc will be available at /redoc

if __name__ == '__main__':
    uvicorn.run("src.api:app", host="0.0.0.0", port=5000, reload=True) 