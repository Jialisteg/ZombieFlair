import pytest
from src.models.building import Building
from src.models.floor import Floor
from src.models.room import Room
from src.models.sensor import Sensor
from src.models.staircase import Staircase

def test_room_creation():
    room = Room(0, 1)  # floor_number, room_number
    assert room.floor_number == 0
    assert room.room_number == 1
    assert not room.has_zombies
    assert room.sensor is not None
    assert isinstance(room.sensor, Sensor)

def test_room_zombie_management():
    room = Room(1, 2)
    assert not room.has_zombies
    
    # Add zombie
    room.add_zombies()
    assert room.has_zombies
    
    # Remove zombie
    room.remove_zombies()
    assert not room.has_zombies
    # El sensor sigue en alerta después de quitar los zombis
    assert room.sensor.is_alert()
    
    # Reset sensor
    room.reset_sensor()
    assert not room.sensor.is_alert()

def test_floor_creation():
    floor = Floor(1, 3)
    assert floor.number == 1
    assert len(floor.rooms) == 3
    assert all(isinstance(room, Room) for room in floor.rooms)
    
    # Test room numbers
    assert floor.rooms[0].number == 0
    assert floor.rooms[1].number == 1
    assert floor.rooms[2].number == 2

def test_floor_room_access():
    floor = Floor(1, 3)
    
    # Test get_room method
    room0 = floor.get_room(0)
    assert room0.number == 0
    
    room1 = floor.get_room(1)
    assert room1.number == 1
    
    # Test room access with invalid index
    with pytest.raises(IndexError):
        floor.get_room(3)  # Only 0, 1, 2 are valid

def test_building_creation():
    building = Building(2, 3)
    
    assert len(building.floors) == 2
    assert all(isinstance(floor, Floor) for floor in building.floors)
    
    # Test floor numbers
    assert building.floors[0].number == 0
    assert building.floors[1].number == 1
    
    # Test room count per floor
    assert len(building.floors[0].rooms) == 3
    assert len(building.floors[1].rooms) == 3

def test_building_floor_access():
    building = Building(2, 3)
    
    # Test get_floor method
    floor0 = building.get_floor(0)
    assert floor0.number == 0
    
    floor1 = building.get_floor(1)
    assert floor1.number == 1
    
    # Test floor access with invalid index
    with pytest.raises(IndexError):
        building.get_floor(2)  # Only 0, 1 are valid

def test_building_room_access():
    building = Building(2, 3)
    
    # Test accessing a room on a specific floor
    room = building.get_floor(0).get_room(1)
    assert room.number == 1
    
    # Add a zombie to a room
    building.get_floor(0).get_room(1).add_zombie()
    assert building.get_floor(0).get_room(1).has_zombie()
    
    # Check another room doesn't have a zombie
    assert not building.get_floor(0).get_room(0).has_zombie()
    assert not building.get_floor(1).get_room(1).has_zombie()

def test_create_room():
    """Prueba para verificar que se puede crear una habitación correctamente."""
    room = Room(1, 2)
    assert room.floor_number == 1
    assert room.room_number == 2
    assert not room.has_zombies
    assert room.sensor is not None
    assert not room.sensor.is_alert()

def test_create_staircase():
    """Prueba para verificar que se puede crear una escalera correctamente."""
    staircase = Staircase(1, 0)
    assert staircase.floor_number == 1
    assert staircase.room_number == 0
    assert not staircase.has_zombies
    assert staircase.sensor is None
    assert len(staircase.connected_floors) == 0

def test_create_floor():
    """Prueba para verificar que se puede crear un piso correctamente."""
    floor = Floor(1, 3)
    assert floor.floor_number == 1
    assert len(floor.rooms) == 3
    
    # La primera habitación debe ser una escalera
    assert isinstance(floor.rooms[0], Staircase)
    
    # El resto de habitaciones deben ser habitaciones normales
    for i in range(1, len(floor.rooms)):
        assert isinstance(floor.rooms[i], Room)

def test_create_building():
    """Prueba para verificar que se puede crear un edificio correctamente."""
    building = Building(2, 3)
    assert len(building.floors) == 2
    
    # Cada piso debe tener 3 habitaciones
    for floor in building.floors:
        assert len(floor.rooms) == 3

def test_staircase_connection():
    """Prueba para verificar que las escaleras están conectadas correctamente entre pisos."""
    building = Building(3, 4)  # 3 pisos, 4 habitaciones por piso (incluyendo escalera)
    
    # Obtener las escaleras de cada piso
    staircase_0 = building.get_floor(0).get_room(0)
    staircase_1 = building.get_floor(1).get_room(0)
    staircase_2 = building.get_floor(2).get_room(0)
    
    # Verificar que todas son instancias de Staircase
    assert isinstance(staircase_0, Staircase)
    assert isinstance(staircase_1, Staircase)
    assert isinstance(staircase_2, Staircase)
    
    # Verificar conexiones entre escaleras
    assert staircase_1 in staircase_0.get_adjacent_rooms()
    assert staircase_0 in staircase_1.get_adjacent_rooms()
    assert staircase_2 in staircase_1.get_adjacent_rooms()
    assert staircase_1 in staircase_2.get_adjacent_rooms()
    
    # Verificar conexiones entre pisos
    assert building.get_floor(1) in staircase_0.get_connected_floors()
    assert building.get_floor(0) in staircase_1.get_connected_floors()
    assert building.get_floor(2) in staircase_1.get_connected_floors()
    assert building.get_floor(1) in staircase_2.get_connected_floors()

def test_building_room_connections():
    """Prueba para verificar que las habitaciones están conectadas correctamente en un edificio."""
    building = Building(2, 3)
    
    # Obtener habitaciones del primer piso
    staircase_0 = building.get_floor(0).get_room(0)
    room_0_1 = building.get_floor(0).get_room(1)
    room_0_2 = building.get_floor(0).get_room(2)
    
    # Obtener habitaciones del segundo piso
    staircase_1 = building.get_floor(1).get_room(0)
    room_1_1 = building.get_floor(1).get_room(1)
    room_1_2 = building.get_floor(1).get_room(2)
    
    # Verificar conexiones horizontales en piso 0
    assert room_0_1 in staircase_0.get_adjacent_rooms()
    assert staircase_0 in room_0_1.get_adjacent_rooms()
    assert room_0_2 in room_0_1.get_adjacent_rooms()
    assert room_0_1 in room_0_2.get_adjacent_rooms()
    
    # Verificar conexiones horizontales en piso 1
    assert room_1_1 in staircase_1.get_adjacent_rooms()
    assert staircase_1 in room_1_1.get_adjacent_rooms()
    assert room_1_2 in room_1_1.get_adjacent_rooms()
    assert room_1_1 in room_1_2.get_adjacent_rooms()
    
    # Verificar conexiones verticales (escaleras)
    assert staircase_1 in staircase_0.get_adjacent_rooms()
    assert staircase_0 in staircase_1.get_adjacent_rooms() 