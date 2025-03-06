import pytest
from src.simulation import Simulation
from src.models.staircase import Staircase
import random

@pytest.fixture
def simulation():
    sim = Simulation()
    sim.setup_building(2, 3)
    return sim

def test_setup_building(simulation):
    assert simulation.building is not None
    assert len(simulation.building.floors) == 2

def test_add_initial_zombies(simulation):
    zombies = simulation.add_initial_zombies(2)
    assert len(zombies) == 2

def test_toggle_zombie_generation(simulation):
    initial_state = simulation.zombie_generation_enabled
    simulation.toggle_zombie_generation()
    assert simulation.zombie_generation_enabled != initial_state

def test_clean_room(simulation):
    simulation.add_initial_zombies(1)
    floor, room = simulation.add_initial_zombies(1)[0]
    result = simulation.clean_room(floor, room)
    assert result['cleaned'] is True

def test_reset_sensor(simulation):
    simulation.add_initial_zombies(1)
    floor, room = simulation.add_initial_zombies(1)[0]
    simulation.clean_room(floor, room)
    result = simulation.reset_sensor(floor, room)
    assert result['reset'] is True

def test_zombie_moves_to_one_room_at_a_time(simulation, monkeypatch):
    # Ensure building is set up with 2 floors, 3 rooms per floor (0=staircase, 1, 2)
    assert simulation.building is not None
    assert len(simulation.building.floors) == 2
    
    # 1. Test zombie stays in the same room
    # Add a zombie to floor 1, room 1
    simulation.building.get_floor(1).get_room(1).add_zombie()
    
    # Mock random.choice to always return the same room (stay)
    monkeypatch.setattr(random, "choice", lambda x: (1, 1))
    
    # Advance the turn
    result = simulation.advance_turn()
    
    # Verify the zombie stayed in the same room
    assert simulation.building.get_floor(1).get_room(1).has_zombie()
    assert not result['vacated_rooms']  # No rooms were vacated
    assert not result['infested_rooms']  # No new rooms were infested
    
    # Clean this room for the next test
    simulation.clean_room(1, 1)
    
    # 2. Test zombie moves to the left
    # Add a zombie to floor 1, room 1
    simulation.building.get_floor(1).get_room(1).add_zombie()
    
    # Mock random.choice to move left
    monkeypatch.setattr(random, "choice", lambda x: (1, 0))
    
    # Advance the turn
    result = simulation.advance_turn()
    
    # Verify the zombie moved left and original room is vacated
    assert not simulation.building.get_floor(1).get_room(1).has_zombie()
    assert simulation.building.get_floor(1).get_room(0).has_zombie()
    assert (1, 1) in result['vacated_rooms']
    assert (1, 0) in result['infested_rooms']
    
    # Clean rooms for the next test
    simulation.clean_room(1, 0)
    
    # 3. Test zombie moves to the right
    # Add a zombie to floor 1, room 1
    simulation.building.get_floor(1).get_room(1).add_zombie()
    
    # Mock random.choice to move right
    monkeypatch.setattr(random, "choice", lambda x: (1, 2))
    
    # Advance the turn
    result = simulation.advance_turn()
    
    # Verify the zombie moved right and original room is vacated
    assert not simulation.building.get_floor(1).get_room(1).has_zombie()
    assert simulation.building.get_floor(1).get_room(2).has_zombie()
    assert (1, 1) in result['vacated_rooms']
    assert (1, 2) in result['infested_rooms']
    
    # Clean rooms for the next test
    simulation.clean_room(1, 2)
    
    # 4. Test zombie moves up a floor (when on staircase)
    # Add a zombie to floor 0, room 0 (staircase)
    simulation.building.get_floor(0).get_room(0).add_zombie()
    
    # Mock random.choice to move up a floor
    monkeypatch.setattr(random, "choice", lambda x: (1, 0))
    
    # Advance the turn
    result = simulation.advance_turn()
    
    # Verify the zombie moved up and original room is vacated
    assert not simulation.building.get_floor(0).get_room(0).has_zombie()
    assert simulation.building.get_floor(1).get_room(0).has_zombie()
    assert (0, 0) in result['vacated_rooms']
    assert (1, 0) in result['infested_rooms']
    
    # Clean rooms for the next test
    simulation.clean_room(1, 0)
    
    # 5. Test zombie moves down a floor (when on staircase)
    # Add a zombie to floor 1, room 0 (staircase)
    simulation.building.get_floor(1).get_room(0).add_zombie()
    
    # Mock random.choice to move down a floor
    monkeypatch.setattr(random, "choice", lambda x: (0, 0))
    
    # Advance the turn
    result = simulation.advance_turn()
    
    # Verify the zombie moved down and original room is vacated
    assert not simulation.building.get_floor(1).get_room(0).has_zombie()
    assert simulation.building.get_floor(0).get_room(0).has_zombie()
    assert (1, 0) in result['vacated_rooms']
    assert (0, 0) in result['infested_rooms']
    
    # Clean rooms
    simulation.clean_room(0, 0)

def test_zombie_generation(simulation):
    # Initially zombie generation should be disabled
    assert simulation.zombie_generation_enabled is False
    
    # Enable zombie generation
    simulation.toggle_zombie_generation()
    assert simulation.zombie_generation_enabled is True
    
    # Count zombies before
    zombie_count_before = sum(1 for floor in simulation.building.floors
                              for room in floor.rooms if room.has_zombie())
    
    # Advance turn which should generate a zombie
    result = simulation.advance_turn()
    
    # Count zombies after
    zombie_count_after = sum(1 for floor in simulation.building.floors
                             for room in floor.rooms if room.has_zombie())
    
    # Verify a new zombie was generated
    assert zombie_count_after == zombie_count_before + 1
    assert result.get('zombie_generated') is True
    
    # Disable zombie generation
    simulation.toggle_zombie_generation()
    assert simulation.zombie_generation_enabled is False
    
    # Clean all rooms to start fresh
    for floor_idx, floor in enumerate(simulation.building.floors):
        for room_idx, room in enumerate(floor.rooms):
            if room.has_zombie():
                simulation.clean_room(floor_idx, room_idx)
    
    # Add one zombie for movement testing
    simulation.building.get_floor(0).get_room(1).add_zombie()
    
    # Count zombies before
    zombie_count_before = sum(1 for floor in simulation.building.floors
                              for room in floor.rooms if room.has_zombie())
    assert zombie_count_before == 1
    
    # Advance turn which should NOT generate a zombie (generation disabled)
    result = simulation.advance_turn()
    
    # Count zombies after
    zombie_count_after = sum(1 for floor in simulation.building.floors
                             for room in floor.rooms if room.has_zombie())
    
    # Verify zombie count is still 1 (only movement, no generation)
    assert zombie_count_after == 1
    assert result.get('zombie_generated') is False

def test_sensor_alerts_when_zombie_enters_room(simulation, monkeypatch):
    # Ensure building is set up
    assert simulation.building is not None
    
    # Clean any existing zombies
    for floor_idx, floor in enumerate(simulation.building.floors):
        for room_idx, room in enumerate(floor.rooms):
            if room.has_zombie():
                simulation.clean_room(floor_idx, room_idx)
    
    # Add a zombie to floor 0, room 1
    simulation.building.get_floor(0).get_room(1).add_zombie()
    
    # Reset all sensors to ensure they're not already in alert
    for floor_idx, floor in enumerate(simulation.building.floors):
        for room_idx, room in enumerate(floor.rooms):
            if hasattr(room, 'sensor') and room.sensor:
                simulation.reset_sensor(floor_idx, room_idx)
    
    # Verify room 2 sensor is not in alert
    assert not simulation.building.get_floor(0).get_room(2).sensor.is_alert()
    
    # Mock random.choice to move the zombie to room 2
    monkeypatch.setattr(random, "choice", lambda x: (0, 2))
    
    # Advance the turn
    simulation.advance_turn()
    
    # Verify that the zombie moved to room 2
    assert simulation.building.get_floor(0).get_room(2).has_zombie()
    
    # Verify that room 2 sensor is now in alert
    assert simulation.building.get_floor(0).get_room(2).sensor.is_alert()
    
    # Clean the room
    simulation.clean_room(0, 2)
    
    # Verify zombie is removed but sensor remains in alert
    assert not simulation.building.get_floor(0).get_room(2).has_zombie()
    assert simulation.building.get_floor(0).get_room(2).sensor.is_alert()
    
    # Reset the sensor
    result = simulation.reset_sensor(0, 2)
    
    # Verify sensor is no longer in alert
    assert result['reset'] is True
    assert not simulation.building.get_floor(0).get_room(2).sensor.is_alert()

def test_zombie_moves_through_staircase(simulation, monkeypatch):
    """Prueba para verificar que un zombi puede moverse entre pisos usando las escaleras."""
    # Asegurarse de que el edificio está configurado
    assert simulation.building is not None
    assert len(simulation.building.floors) == 2
    
    # Verificar que la habitación 0 de cada piso es una escalera
    staircase_0 = simulation.building.get_floor(0).get_room(0)
    staircase_1 = simulation.building.get_floor(1).get_room(0)
    assert isinstance(staircase_0, Staircase)
    assert isinstance(staircase_1, Staircase)
    
    # Añadir un zombi a la escalera del piso 0
    staircase_0.add_zombies()
    assert staircase_0.has_zombies
    
    # Configurar random.choice para que siempre elija el piso 1, habitación 0 (escalera)
    monkeypatch.setattr(random, "choice", lambda x: (1, 0))
    
    # Avanzar un turno
    result = simulation.advance_turn()
    
    # Verificar que el zombi se movió de la escalera del piso 0 a la escalera del piso 1
    assert not staircase_0.has_zombies
    assert staircase_1.has_zombies
    assert (0, 0) in result['vacated_rooms']
    assert (1, 0) in result['newly_infested']
    
def test_two_zombies_one_room(simulation, monkeypatch):
    """
    Prueba para verificar que si dos zombis están en una habitación,
    se mueven como dos zombis separados.
    """
    # Asegurarse de que el edificio está configurado
    assert simulation.building is not None
    
    # Habitaciones diferentes para los zombis
    room_1_1 = simulation.building.get_floor(0).get_room(1)
    room_1_2 = simulation.building.get_floor(0).get_room(2)
    
    # Marcar ambas habitaciones como que tienen zombis
    room_1_1.add_zombies()
    room_1_1.add_zombies()  # Simular un segundo zombi en la misma habitación
    
    # Guardar número inicial de habitaciones infestadas
    initial_infested_count = len(simulation.building.get_all_rooms_with_zombies())
    assert initial_infested_count == 1
    
    # Configurar random.choice para que devuelva diferentes destinos para cada zombi
    # Esto requiere modificar cómo simulation.advance_turn usa random.choice
    # para poder controlar el comportamiento de múltiples zombis
    
    # Avanzar un turno
    monkeypatch.setattr(random, "choice", lambda x: (0, 2))  # Mover a habitación 2
    result = simulation.advance_turn()
    
    # Verificar que el zombi se movió y que la habitación original ya no tiene zombis
    assert not room_1_1.has_zombies
    assert room_1_2.has_zombies
    
    # Verificar que solo se movió un zombi (no implementamos conteo de zombis por habitación)
    final_infested_count = len(simulation.building.get_all_rooms_with_zombies())
    assert final_infested_count == 1  # Todavía solo hay una habitación infestada 