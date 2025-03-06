import pytest
from src.models.building import Building, Floor, Room
from src.models.sensor import Sensor

def test_room_creation():
    room = Room(0, "Test Room")
    assert room.number == 0
    assert room.name == "Test Room"
    assert not room.has_zombie()
    assert room.sensor is not None
    assert isinstance(room.sensor, Sensor)

def test_room_zombie_management():
    room = Room(1, "Zombie Room")
    assert not room.has_zombie()
    
    # Add zombie
    room.add_zombie()
    assert room.has_zombie()
    
    # Remove zombie
    room.remove_zombie()
    assert not room.has_zombie()

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