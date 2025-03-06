from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
import os
import sys
import json

# Agregar el directorio raíz al path para poder importar desde src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la clase Simulation desde el proyecto original
from src.simulation import Simulation

# Crear la instancia de FastAPI
app = FastAPI(
    title="Zombie Building Simulation API",
    description="API para la Simulación de Edificio con Zombies",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear una instancia global de Simulation para ser compartida entre solicitudes
simulation = Simulation()

# Modelos Pydantic para validar solicitudes
class BuildingConfig(BaseModel):
    floors: int = Field(3, ge=1, description="Número de pisos")
    roomsPerFloor: int = Field(5, ge=1, description="Habitaciones por piso")
    initialZombies: int = Field(1, ge=0, description="Zombies iniciales")

class RoomAction(BaseModel):
    floor: int = Field(..., ge=0, description="Índice del piso")
    room: int = Field(..., ge=0, description="Índice de la habitación")

class AutoRunConfig(BaseModel):
    run: bool = Field(False, description="Activar ejecución automática")

# Rutas de la API
@app.get("/api/simulation/state", response_model=Dict[str, Any])
async def get_simulation_state():
    """Obtener el estado actual de la simulación"""
    if not simulation.building:
        raise HTTPException(status_code=404, detail="No hay edificio configurado")
    
    state = simulation.get_building_state()
    
    # Agregar información adicional para el frontend
    state['game_over'] = simulation.is_game_over()
    state['game_over_reason'] = simulation.game_over_reason
    state['zombie_generation_enabled'] = simulation.zombie_generation_enabled
    
    # Agregar información del practicante si existe
    if simulation.practicante:
        state['practicante'] = {
            'floor': simulation.practicante.floor_number,
            'room': simulation.practicante.room_number
        }
    else:
        state['practicante'] = None
    
    # Agregar estructura del edificio
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
            
            # Agregar datos del sensor para habitaciones regulares
            if not room_data['is_staircase']:
                room_data['sensor_alert'] = room.sensor.is_alert()
            
            floor_data.append(room_data)
        building_data.append(floor_data)
    
    state['building'] = building_data
    
    return state

@app.post("/api/simulation/setup", response_model=Dict[str, Any])
async def setup_simulation(config: BuildingConfig):
    """Configurar un nuevo edificio para la simulación"""
    result = simulation.setup_building(config.floors, config.roomsPerFloor)
    zombies_added = simulation.add_initial_zombies(config.initialZombies)
    
    return {
        "success": True,
        "building": result,
        "zombies_added": zombies_added
    }

@app.post("/api/simulation/advance", response_model=Dict[str, Any])
async def advance_simulation():
    """Avanzar la simulación un turno"""
    if not simulation.building:
        raise HTTPException(status_code=404, detail="No hay edificio configurado")
    
    result = simulation.advance_turn()
    return result

@app.post("/api/simulation/add-zombie", response_model=Dict[str, Any])
async def add_zombie():
    """Agregar un zombie en una habitación aleatoria"""
    if not simulation.building:
        raise HTTPException(status_code=404, detail="No hay edificio configurado")
    
    result = simulation.add_random_zombie()
    return result

@app.post("/api/simulation/add-practicante", response_model=Dict[str, Any])
async def add_practicante():
    """Agregar un practicante en una habitación sin zombies"""
    if not simulation.building:
        raise HTTPException(status_code=404, detail="No hay edificio configurado")
    
    result = simulation.add_practicante()
    return result

@app.post("/api/simulation/clean-room", response_model=Dict[str, Any])
async def clean_room(room_data: RoomAction):
    """Limpiar una habitación (eliminar zombies)"""
    if not simulation.building:
        raise HTTPException(status_code=404, detail="No hay edificio configurado")
    
    result = simulation.clean_room(room_data.floor, room_data.room)
    return result

@app.post("/api/simulation/reset-sensor", response_model=Dict[str, Any])
async def reset_sensor(room_data: RoomAction):
    """Restablecer un sensor en una habitación"""
    if not simulation.building:
        raise HTTPException(status_code=404, detail="No hay edificio configurado")
    
    result = simulation.reset_sensor(room_data.floor, room_data.room)
    return result

@app.post("/api/simulation/toggle-zombie-generation", response_model=Dict[str, Any])
async def toggle_zombie_generation():
    """Activar/desactivar la generación automática de zombies"""
    enabled = simulation.toggle_zombie_generation()
    return {"zombie_generation_enabled": enabled}

@app.post("/api/simulation/use-secret-weapon", response_model=Dict[str, Any])
async def use_secret_weapon():
    """Usar el arma secreta para limpiar múltiples habitaciones"""
    if not simulation.building:
        raise HTTPException(status_code=404, detail="No hay edificio configurado")
    
    cleaned_count = simulation.use_secret_weapon()
    return {"cleaned_count": cleaned_count}

@app.post("/api/simulation/reset", response_model=Dict[str, bool])
async def reset_simulation():
    """Reiniciar la simulación"""
    global simulation
    simulation = Simulation()
    return {"success": True} 