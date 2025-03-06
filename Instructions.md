Ok let's try to solve this in under an hour. Here are my insights so far:

1.- I need to solve the problem from "Enunciado.md" (Create all the files and folders neccesary).

2.- All the prints and documentation (docstrings and comments) must be in SPANISH.

3.- Debugging and logging: We need to add a "DEBUG" feature so that we can know at all times (if desired by the user) what is happening within the simulation. Add a "logs" folder and store the debug info there.

4.- Constantly update Readme.md with instructions for the user. 

5.- User interface: We have to explain the instructions of the game before playing to improve user experience.  

**Movement Logic**
    - **Adjacent Rooms**: Horizontal movement (same floor) can occur between rooms with contiguous room_number values (e.g., room 0 is adjacent to room 1).
    - **Between Floors**: Vertical movement. We will create an extra class called `Staircase` which will allow a zombie to move one floor upwards or downwards. A staircase will behave like a room, but will have no sensors, and it must have it's own Icon.
    - When zombies enter a new room, the corresponding sensor switches to `alert`.

6.- Testing: There will be a lot of bugs, and we need to write the right tests in order to be able to isolate and understand each core functionality (and fix it).

Here are important tests that I can think of: 

    -test_zombie_movement: We need to test that a Zombie can move to one room at a time (if he's in a room he has 3 possible movements, and if he's in a Staircase there are 5 possible movements). Try it on a Example building of 3x3, or greater.

    -test_zombie_generation: If enabled, there should be a spawn rate of one zombie per turn.

    -test_sensor_alerts_when_zombie_enters_room:  If a zombie enters a room, the sensor must be activated.

    -test_two_zombies_one_room: If two zombies are in one room, they should not merge as one. They have to keep moving a two separate zombies.
