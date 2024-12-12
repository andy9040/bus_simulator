# Bus Route Simulator

## Description
The Bus Route Simulator is an interactive application developed using Python and Pygame. It allows users to simulate bus routes, generate users, and manage the movement of buses and users within a graphical environment. The application visualizes user activity and bus capacity while providing an engaging and intuitive interface.

## Features
- **Node Creation**: Add nodes to define bus stops on the map by clicking on the screen.
- **User Generation**: Generate users randomly across the map who will move toward their nearest bus stop.
- **Dynamic Bus Routes**: Create routes for buses to traverse and manage their movement along the route.
- **User Interaction**: Users can board and alight from buses at specified stops.
- **Capacity Management**: Limit the number of users on the bus based on its capacity.
- **Visualization**: Real-time updates on user positions, bus movements, and statistics for satisfied users.

## Installation
1. Clone this repository or download the source code:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```
2. Install the required Python dependencies:
    ```bash
    pip install pygame
    ```

## Usage
1. Place a map image named `map.png` in the same directory as the script.
2. Run the simulator:
    ```bash
    python <script-name>.py
    ```
3. Interact with the simulation using:
    - **Mouse Click**: Add bus stops (nodes) on the map.
    - **`U` Key**: Generate 100 users randomly on the map.
    - **`B` Key**: Start the bus simulation.

## Controls
| Action          | Control       |
|-----------------|---------------|
| Add a Node      | Left Mouse Click |
| Generate Users  | Press `U`     |
| Start Bus Route | Press `B`     |

## Key Classes
### Node
Represents a bus stop in the simulation.
- Attributes:
  - `x`, `y`: Coordinates on the map.
  - `bus_stopped`: Boolean indicating if the bus is currently at the node.
  - `stop_time_start`: Timestamp of when the bus stopped.
- Method:
  - `draw()`: Visualizes the node and its user activity.

### User
Represents a passenger in the simulation.
- Attributes:
  - `position`: Current position on the map.
  - `target_node`: The user's destination node.
  - `on_bus`: Boolean indicating if the user is on the bus.
  - `bus_stops_remaining`: Number of stops left for the user.
  - `done`: Boolean indicating if the user has completed their journey.
- Method:
  - `draw()`: Visualizes the user on the map.

## Statistics Display
- **Users on Bus**: Displays the number of users currently on the bus.
- **Satisfied Users**: Shows the count of users who have completed their journey.
- **Total Users**: Displays the total number of users generated during the simulation.

## Customization
- **`BUS_CAPACITY`**: Adjust the maximum capacity of the bus.
- **`USER_GENERATE`**: Modify the number of users generated per click.
- **Node Radius**: Change the size of the nodes by updating the `RADIUS` variable.

## Future Enhancements
- Add support for multiple buses.
- Implement realistic pathfinding for users.
- Provide detailed metrics and analytics for the simulation.
- Enable saving and loading of simulation states.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Credits
Developed using Python and Pygame.
