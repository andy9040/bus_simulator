import pygame
import sys
import math
import time
import random

# Initialize Pygame
pygame.init()
image = pygame.image.load('map.png')  
# Constants
WIDTH, HEIGHT = 1300, 800
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255,0,255)
WHITE = (255,255,255)
RADIUS = 10  # User node radius
STOP_TIME = 0.5  # Stop time at each node in seconds
USER_GENERATE = 100 # Number of users to generate per pressing 'U'
bus_speed = .5
num_clicks = 0
BUS_CAPACITY = 60 # Max Bus Capacity

# Create a window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bus Route Simulator')

nodes = []  # List to store nodes
lines = []  # List to store lines between nodes
users = []  # List to store user objects

# Define Node class
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bus_stopped = False
        self.stop_time_start = 0

    def draw(self):

        users_waiting = 0 
        for user in users:
            if not user.on_bus and not user.done and user.target_node == self:
                users_waiting += 1 

        # Default color is white
        node_color = (0, 0, 255)
        intensity = min(255, users_waiting * 20)
        node_color = (intensity, 0, 255-intensity)

        radius = RADIUS * (1+users_waiting/10)

        pygame.draw.circle(window, node_color, (self.x, self.y), radius)


# Define User class
class User:
    def __init__(self, pos):
        self.position = list(pos)
        self.target_node = None
        self.on_bus = False
        self.bus_stops_remaining = random.randint(1, 5)  # Random number of stops to stay on bus
        self.done = False

    def draw(self):
        if not self.done:
            if not self.on_bus:
                pygame.draw.circle(window, RED, (int(self.position[0]), int(self.position[1])), RADIUS // 2)  # Adjusted radius for user nodes
        else:
            pygame.draw.circle(window, BLUE, (10,10), RADIUS // 2)

# Create nodes function
def create_nodes(pos):
    nodes.append(Node(pos[0], pos[1]))

# Function to find the closest node to a position
def find_closest_node(pos):
    closest_node = None
    min_distance = float('inf')

    for node in nodes:
        distance = math.sqrt((node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_node = node

    return closest_node

# Create a route for the bus to travel
def create_route():
    global lines
    lines = [(node.x, node.y) for node in nodes]

# Game loop
running = True
reverse = False  # Flag to reverse the route
creating_bus = False  # Flag to create bus
bus_position = None  # Position of the bus along the route
current_route_index = 0  # Index to traverse the route

# Users are stationary initially
generating_users = False

def display():
    #counter
    users_on_bus = sum(1 for user in users if user.on_bus)

    # Draw counter for users on the bus
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Users on bus: {users_on_bus}', True, WHITE)
    text_satisfied = font.render(f'Satisfied users: {sum(1 for user in users if user.done)}', True, WHITE)
    text_total = font.render(f'Total users: {USER_GENERATE*num_clicks}', True, WHITE)

    window.blit(text, (10, 10))  # Display at the top-left corner
    window.blit(text_satisfied, (10, 50))
    window.blit(text_total, (10, 90))


    pygame.display.flip()

while running:
    window.fill(BLACK)
    window.blit(image, (250, 10))  

    print("Users on bus", sum(1 for user in users if user.on_bus))
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            create_nodes(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                generating_users = True  # Start generating users but keep them stationary
                num_clicks += 1
                for _ in range(USER_GENERATE):
                    user = User((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
                    user.target_node = None  # Set target_node to None initially
                    users.append(user)
            elif event.key == pygame.K_b:
                generating_users = False  # Stop generating users and start moving them
                creating_bus = True
                for user in users:
                    user.target_node = find_closest_node(user.position)
                create_route()

    # Draw nodes and lines
    for node in nodes:
        node.draw()

    for i in range(len(lines) - 1):
        pygame.draw.line(window, GREEN, lines[i], lines[i + 1], 2)

    # Move and handle users
    for user in users:
        if not user.on_bus:
            if user.target_node:
                dx = user.target_node.x - user.position[0]
                dy = user.target_node.y - user.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance > 0.5:
                    user.position[0] += (dx / distance) * 2
                    user.position[1] += (dy / distance) * 2
                else:
                    user.position = [user.target_node.x, user.target_node.y]

        else:
            if user.bus_stops_remaining <= 0:
                user.on_bus = False
                user.done = True
                user.position = [user.target_node.x, user.target_node.y]

        user.draw()
    
    print()
    # Bus movement logic
    if creating_bus:

        #counter
        users_on_bus = sum(1 for user in users if user.on_bus)
        done_users = sum(1 for user in users if user.done)
        print("On Bus: ",users_on_bus)
        print("Done: ", done_users)

        # Draw counter for users on the bus
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Users on bus: {users_on_bus}', True, GREEN)
        window.blit(text, (10, 10))  # Display at the top-left corner

        if bus_position is None:
            bus_position = lines[0]

        if reverse:
            dx = lines[current_route_index - 1][0] - bus_position[0]
            dy = lines[current_route_index - 1][1] - bus_position[1]
        else:
            dx = lines[current_route_index + 1][0] - bus_position[0]
            dy = lines[current_route_index + 1][1] - bus_position[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > bus_speed:
            bus_position = (
                bus_position[0] + (dx / distance) * bus_speed,
                bus_position[1] + (dy / distance) * bus_speed,
            )
        else:

            next_index = current_route_index + 1 if not reverse else current_route_index - 1
            if 0 <= next_index < len(nodes):
                current_route_index = next_index
                
                # Check if any users are waiting at the current node
                for user in users:
                    users_on_bus = sum(1 for user in users if user.on_bus)
                    print("Space on bus:", BUS_CAPACITY-users_on_bus)

                    if (user.target_node == nodes[current_route_index] and not user.on_bus and not user.done and users_on_bus<BUS_CAPACITY):
                        user.on_bus = True
                        # user.bus_stops_remaining = random.randint(1, 5)  # Set random stops to stay on bus
                        
                        # Update the target node for the user
                        if 0 <= current_route_index + 1 < len(nodes) and not reverse:
                            user.target_node = nodes[current_route_index + 1]
                        elif 0 <= current_route_index - 1 < len(nodes) and reverse:
                            user.target_node = nodes[current_route_index - 1]
                    
                    elif user.on_bus:
                        print("STOP REMAINING")
                        user.bus_stops_remaining -= 1
            
            if current_route_index <= 0:
                reverse = False
                current_route_index = 0
            elif current_route_index >= len(lines) - 1:
                reverse = True
                current_route_index = len(lines) - 1
            


        pygame.draw.circle(window, (0, 255, 0), (int(bus_position[0]), int(bus_position[1])), RADIUS)

    display()

# Quit Pygame
pygame.quit()
sys.exit()

