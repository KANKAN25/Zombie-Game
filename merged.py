import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
TOP_HEIGHT = 150
BOTTOM_HEIGHT = HEIGHT - TOP_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ISKOmbie")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
GREEN = (0, 128, 0)

# Define colors for the gradient
horizon_color = (25, 127, 127)  # Orange
sky_color = (255, 165, 0)       # Orange

# Default circle parameters
default_radius = 100
default_speed = 0.05
default_weight = 1.0

# Center point coordinates in the bottom section
center_x = WIDTH // 2
center_y = TOP_HEIGHT + (BOTTOM_HEIGHT // 2)

# Speed of the center point movement
move_speed = 3

class Slider:
    def __init__(self, x, y, w, min_val, max_val, start_val, label=''):
        self.rect = pygame.Rect(x, y, w, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.grabbed = False
        self.handle_rect = pygame.Rect(x + (w * (start_val - min_val) / (max_val - min_val)) - 5, y - 5, 10, 20)
        self.label = label
        self.start_time = 0
        self.end_time = 0
        self.release_time = 0
        self.drag_duration = 0
        self.initial_speed = start_val
        self.final_speed = start_val
        self.tangential_acc = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.grabbed = True
                self.start_time = pygame.time.get_ticks()
                self.initial_speed = self.value
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.grabbed:
                self.grabbed = False
                self.end_time = pygame.time.get_ticks()
                self.drag_duration = (self.end_time - self.start_time) / 1000  # in seconds
                self.final_speed = self.value
                if self.drag_duration > 0:
                    self.tangential_acc = (self.final_speed*100 - self.initial_speed*100) / self.drag_duration
                else:
                    self.tangential_acc = 0
                self.release_time = pygame.time.get_ticks()
                print(f"Slider '{self.label}' was dragged for {self.drag_duration} seconds with tangential acceleration {self.tangential_acc} m/s²")
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                new_x = event.pos[0]
                new_x = max(self.rect.x, min(new_x, self.rect.x + self.rect.width))
                self.handle_rect.x = new_x - 5
                self.value = self.min_val + (self.max_val - self.min_val) * ((new_x - self.rect.x) / self.rect.width)
                self.final_speed = self.value
                current_time = pygame.time.get_ticks()
                self.drag_duration = (current_time - self.start_time) / 1000  # in seconds
                if self.drag_duration > 0:
                    self.tangential_acc = (self.final_speed*100 - self.initial_speed*100) / self.drag_duration

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.grabbed and current_time - self.release_time > 3000:  # 3000 milliseconds = 3 seconds
            self.tangential_acc = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLUE, self.handle_rect)

    def get_value(self):
        return self.value

    def get_tangential_acc(self):
        return self.tangential_acc

class OutputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = pygame.font.Font(None, 18).render(text, True, self.color)

    def update(self, text):
        self.text = text
        self.txt_surface = pygame.font.Font(None, 18).render(text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def calculate_centripetal_acceleration(radius, speed):
    if radius == 0:
            return float('inf')
    else:
        return (speed ** 2) / radius

def calculate_centripetal_force(weight, radius, speed):
    return weight * calculate_centripetal_acceleration(radius, speed)

def calculate_angular_velocity(speed, radius):
    if radius == 0:
        return float('inf')
    else:
        return speed / radius

def calculate_angular_acc(tangential_acc, radius):
    if radius == 0:
        return float('inf')
    else:
        return tangential_acc / radius
    
def calculate_net_force(weight, tangential_acc, centripetal_acc):
    return weight * math.sqrt(tangential_acc**2 + centripetal_acc**2)


def draw_scene(radius, angle, center_x, center_y, ball_image, ball_rect, character_img):
    # Blit the background image for the bottom section
    screen.blit(background_bottom_image, (0, TOP_HEIGHT))

    # Calculate circle position
    circle_x = center_x + radius * math.cos(angle)
    circle_y = center_y + radius * math.sin(angle)

    # Draw center point
    pygame.draw.circle(screen, BLACK, (center_x, center_y), 5)

    # Draw the ball image at the calculated position
    screen.blit(ball_image, (circle_x - ball_rect.width // 2, circle_y - ball_rect.height // 2))

    # Draw line connecting center point and circle
    pygame.draw.line(screen, (34, 40, 49), (center_x, center_y), (int(circle_x), int(circle_y)), 2)

    # Blit the character onto the screen
    screen.blit(character_img, (center_x - character_img.get_width() // 2, center_y - character_img.get_height() // 2))

def draw_label(text, x, y):
    font = pygame.font.Font(None, 18)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))


def create_wave(num_zombies, zombie_images, zombie_images_2, zombie_images_4, zombie_images_3):
    zombie_rect_offsetX = 5
    zombie_rect_offsetY = 5
    zombie_rect_width = 30
    zombie_rect_height = 50
    zombies = []
    directions = ['front', 'back', 'left', 'right']
    for _ in range(num_zombies):
        zombie_rect = zombie_images['front'][0].get_rect()
        # Adjust the dimensions of the zombie rectangle
        zombie_rect = pygame.Rect(zombie_rect.x + zombie_rect_offsetX, zombie_rect.y + zombie_rect_offsetY, zombie_rect_width, zombie_rect_height)
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            zombie_rect.x = random.randint(0, 800)
            zombie_rect.y = 150
        elif edge == 'bottom':
            zombie_rect.x = random.randint(0, 800)
            zombie_rect.y = 450
        elif edge == 'left':
            zombie_rect.x = -50
            zombie_rect.y = random.randint(150, 400)
        elif edge == 'right':
            zombie_rect.x = 850
            zombie_rect.y = random.randint(150, 400)

        zombie_image_choice = random.choice([(zombie_images, int(random.uniform(1, 400))), (zombie_images_2, int(random.uniform(1, 400))), (zombie_images_4, int(random.uniform(1, 400))), (zombie_images_3, int(random.uniform(1, 400)))])
        chosen_images, health = zombie_image_choice
        direction = random.choice(directions)

        zombies.append({
            'rect': zombie_rect,
            'health': health,
            'max_health': health,
            'images': chosen_images,
            'direction': direction
        })
    return zombies

# Function to calculate the offset for zombie movement
def calculate_offset(zombie_info, zombies):
    offset_x = 0
    offset_y = 0
    zombie_rect = zombie_info['rect']
    for other_zombie_info in zombies:
        if other_zombie_info != zombie_info:
            other_zombie_rect = other_zombie_info['rect']
            dx = other_zombie_rect.x - zombie_rect.x
            dy = other_zombie_rect.y - zombie_rect.y
            distance = math.hypot(dx, dy)
            if distance < 50:  # Adjust this distance as needed
                offset_x -= dx / distance
                offset_y -= dy / distance
    return offset_x, offset_y


# Load zombie images
zombie_front_images = [
    pygame.image.load('zombie_front.png').convert_alpha(),
    pygame.image.load('zombie_front2.png').convert_alpha(),
]
zombie_back_images = [
    pygame.image.load('zombie_back.png').convert_alpha(),
    pygame.image.load('zombie_back2.png').convert_alpha(),
]
zombie_left_images = [
    pygame.image.load('zombie_left.png').convert_alpha(),
    pygame.image.load('zombie_left2.png').convert_alpha(),
]
zombie_right_images = [
    pygame.image.load('zombie_right.png').convert_alpha(),
    pygame.image.load('zombie_right2.png').convert_alpha(),
]

zombie2_front_images = [
    pygame.image.load('zombie2_front.png').convert_alpha(),
    pygame.image.load('zombie2_front2.png').convert_alpha(),
]
zombie2_back_images = [
    pygame.image.load('zombie2_back.png').convert_alpha(),
    pygame.image.load('zombie2_back2.png').convert_alpha(),
]
zombie2_left_images = [
    pygame.image.load('zombie2_left.png').convert_alpha(),
    pygame.image.load('zombie2_left2.png').convert_alpha(),
]
zombie2_right_images = [
    pygame.image.load('zombie2_right.png').convert_alpha(),
    pygame.image.load('zombie2_right2.png').convert_alpha(),
]

zombie3_front_images = [
    pygame.image.load('zombie3_right1.png').convert_alpha(),
]
zombie3_back_images = [
    pygame.image.load('zombie3_back.png').convert_alpha()
]
zombie3_left_images = [
    pygame.image.load('zombie3_left1.png').convert_alpha(),
    pygame.image.load('zombie3_left2.png').convert_alpha(),
]
zombie3_right_images = [
    pygame.image.load('zombie3_right1.png').convert_alpha(),
    pygame.image.load('zombie3_right2.png').convert_alpha(),
    pygame.image.load('zombie3_right3.png').convert_alpha(),
    pygame.image.load('zombie3_right4.png').convert_alpha(),
]

zombie4_front_images = [
    pygame.image.load('zombie4_front.png').convert_alpha(),
]
zombie4_back_images = [
    pygame.image.load('zombie4_back2.png').convert_alpha(),
    pygame.image.load('zombie4_back3.png').convert_alpha(),
]
zombie4_left_images = [
    pygame.image.load('zombie4_left.png').convert_alpha(),
    pygame.image.load('zombie4_left2.png').convert_alpha(),
]
zombie4_right_images = [
    pygame.image.load('zombie4_right.png').convert_alpha(),
    pygame.image.load('zombie4_right2.png').convert_alpha(),
]

# Scale images
def scale_images(images, size):
    return [pygame.transform.scale(image, size) for image in images]

zombie_front_images = scale_images(zombie_front_images, (40, 40))
zombie_back_images = scale_images(zombie_back_images, (40, 40))
zombie_left_images = scale_images(zombie_left_images, (40, 40))
zombie_right_images = scale_images(zombie_right_images, (40, 40))

zombie2_front_images = scale_images(zombie2_front_images, (40, 40))
zombie2_back_images = scale_images(zombie2_back_images, (40, 40))
zombie2_left_images = scale_images(zombie2_left_images, (40, 40))
zombie2_right_images = scale_images(zombie2_right_images, (40, 40))

zombie3_front_images = scale_images(zombie3_front_images, (80, 80))
zombie3_back_images = scale_images(zombie3_back_images, (80, 80))
zombie3_left_images = scale_images(zombie3_left_images, (80, 80))
zombie3_right_images = scale_images(zombie3_right_images, (80, 80))

zombie4_front_images = scale_images(zombie4_front_images, (40, 40))
zombie4_back_images = scale_images(zombie4_back_images, (40, 40))
zombie4_left_images = scale_images(zombie4_left_images, (40, 40))
zombie4_right_images = scale_images(zombie4_right_images, (40, 40))


zombie_images = {
    'front': zombie_front_images,
    'back': zombie_back_images,
    'left': zombie_left_images,
    'right': zombie_right_images
}

zombie2_images = {
    'front': zombie2_front_images,
    'back': zombie2_back_images,
    'left': zombie2_left_images,
    'right': zombie2_right_images
}

zombie3_images = {
    'front': zombie3_front_images,
    'back': zombie3_back_images,
    'left': zombie3_left_images,
    'right': zombie3_right_images
}

zombie4_images = {
    'front': zombie4_front_images,
    'back': zombie4_back_images,
    'left': zombie4_left_images,
    'right': zombie4_right_images
}


# Game state variables
level = 1
base_num_zombies = 5  # Base number of zombies
zombies = create_wave(base_num_zombies * level, zombie_images, zombie2_images, zombie4_images, zombie3_images)

# Main game loop
running = True
clock = pygame.time.Clock()
angle = 0
radius = default_radius
speed = default_speed
weight = default_weight

zombie_speed = 0.56  # Speed of the zombies
frame_count = 0

# Game over
game_over = False

# Fonts
font = pygame.font.Font(None, 18)

def get_zombie_image(zombie_info, frame_count):
    direction = zombie_info['direction']
    images = zombie_info['images'][direction]
    index = (frame_count // 20) % len(images)  # Animation speed of the zombies
    return images[index]

# Create sliders
radius_slider = Slider(360, 50, 300, 10, 200, default_radius, "Radius (m):")
speed_slider = Slider(360, 90, 300, 0.01, 0.2, default_speed, "Tangential velocity (m/s):")
weight_slider = Slider(360, 130, 300, 0.5, 5.0, default_weight, "Weight (kg):")

sliders = [radius_slider, speed_slider, weight_slider]

output_box_height = 20
# Create output boxes for uniform circular motion
angular_velocity_output = OutputBox(20, 40, 250, output_box_height, "Angular Velocity (rad/s): ")
centripetal_acc_output = OutputBox(20, 70, 250, output_box_height, "Centripetal Acceleration (m/s^2): ")
centripetal_force_output = OutputBox(20, 100, 250, output_box_height, "Centripetal Force (N): ")

#create ouptut boxes for non uniform circular motion
angular_acc_output = OutputBox(530, 40, 250, output_box_height, "Angular Acceleration (rad/s): ")
tangential_acc_output = OutputBox(530, 70, 250, output_box_height, "Tangential Acceleration (m/s^2): ")
net_force_output = OutputBox(530, 100, 250, output_box_height, "Net Force (N): ")

output_boxes = [angular_velocity_output, centripetal_acc_output, centripetal_force_output, angular_acc_output, tangential_acc_output, net_force_output]

# Load the background image for the bottom section
background_bottom_image = pygame.image.load("background_bottom.png").convert_alpha()
background_bottom_image = pygame.transform.scale(background_bottom_image, (WIDTH, BOTTOM_HEIGHT))

# Load the images for character directions
direction_images = {
    "stationary": pygame.image.load("main_stationary.png").convert_alpha(),
    "north": pygame.image.load("main_moving_north.png").convert_alpha(),
    "south": pygame.image.load("main_moving_south.png").convert_alpha(),
    "east": pygame.image.load("main_moving_east.png").convert_alpha(),
    "west": pygame.image.load("main_moving_west.png").convert_alpha(),
    "northeast": pygame.image.load("main_moving_northeast.png").convert_alpha(),
    "northwest": pygame.image.load("main_moving_northwest.png").convert_alpha(),
    "southeast": pygame.image.load("main_moving_southeast.png").convert_alpha(),
    "southwest": pygame.image.load("main_moving_southwest.png").convert_alpha()
}

# Scale all direction images to the same size as the stationary image
scale_factor = 0.3
stationary_image = pygame.transform.scale(direction_images["stationary"], (int(direction_images["stationary"].get_width() * scale_factor), int(direction_images["stationary"].get_height() * scale_factor)))

for key in direction_images:
    direction_images[key] = pygame.transform.scale(direction_images[key], (stationary_image.get_width(), stationary_image.get_height()))

character_image = direction_images["stationary"]

# Define column widths
COLUMN_WIDTH = WIDTH // 3

# Create and position sliders
radius_slider = Slider(COLUMN_WIDTH + 17, 40, 200, 10, 200, default_radius, "Radius:")
speed_slider = Slider(COLUMN_WIDTH + 17, 80, 200, 0.01, 0.2, default_speed, "Speed:")
weight_slider = Slider(COLUMN_WIDTH + 17, 120, 200, 0.5, 5.0, default_weight, "Weight (kg):")


sliders = [radius_slider, speed_slider, weight_slider]




# Define initial position and size of the character's rect
character_rect = character_image.get_rect(center=(center_x, center_y))

#Define offsetX, offsetY, width, and height for character and zombie collision rectangles
char_rect_offsetX = 10
char_rect_offsetY = 10
char_rect_width = 30
char_rect_height = 50

# Adjust the dimensions of the character rectangle
character_rect = pygame.Rect(character_rect.x + char_rect_offsetX, character_rect.y + char_rect_offsetY, char_rect_width, char_rect_height)

# Load heart image for lives
heart_image = pygame.image.load("heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Adjust size if necessary

# Load the image for the ball
ball_image = pygame.image.load("ball.png").convert_alpha()

# Define the initial size of the ball
initial_ball_size = 50

# Create a rect for the ball image and scale it
ball_rect = pygame.Rect(0, 0, initial_ball_size, initial_ball_size)
ball_image = pygame.transform.scale(ball_image, (initial_ball_size, initial_ball_size))

# Define constants for health and lives
MAX_HEALTH = 100
MAX_LIVES = 3
DAMAGE_PER_HIT = 20  # Adjust damage as needed

# Initialize character's health and lives
current_health = MAX_HEALTH
current_lives = MAX_LIVES

# Define cooldown variables
last_damage_time = 0
damage_cooldown = 500  # Cooldown time in milliseconds (e.g., 500ms)
bounce_distance = 40  # Distance to bounce away upon collision


# Define function to handle character damage
def handle_damage():
    global current_health, current_lives, DAMAGE_PER_HIT, game_over, last_damage_time
    current_time = pygame.time.get_ticks()
    if current_time - last_damage_time > damage_cooldown:
        current_health -= DAMAGE_PER_HIT
        print("current: " + str(current_health))
        last_damage_time = current_time
        if current_health <= 0:
            current_lives -= 1
            if current_lives > 0:
                current_health = MAX_HEALTH
                # Teleport character to a safe area away from zombies
                character_rect.x = random.randint(0, WIDTH)
                character_rect.y = random.randint(TOP_HEIGHT, HEIGHT)
            else:
                game_over = True  # End the game if no lives left
        # Bounce character away from the zombie
        bounce_away()

# Function to bounce the zombie away from the ball
def bounce_away_from_ball(zombie_rect, ball_rect):
    # Calculate the direction to bounce away from the ball
    ball_center_x = ball_rect.centerx
    ball_center_y = ball_rect.centery
    zombie_center_x = zombie_rect.centerx
    zombie_center_y = zombie_rect.centery

    dx = zombie_center_x - ball_center_x
    dy = zombie_center_y - ball_center_y
    distance = math.hypot(dx, dy)

    if distance != 0:
        dx /= distance
        dy /= distance

    # Bounce the zombie
    zombie_rect.x += int(dx * bounce_distance)
    zombie_rect.y += int(dy * bounce_distance)

def bounce_away():
    global character_rect
    # Calculate the direction to bounce away from the zombie
    zombie_center_x = zombie_rect.centerx
    zombie_center_y = zombie_rect.centery
    character_center_x = character_rect.centerx
    character_center_y = character_rect.centery

    dx = character_center_x - zombie_center_x
    dy = character_center_y - zombie_center_y
    distance = math.hypot(dx, dy)

    if distance != 0:
        dx /= distance
        dy /= distance

    # Bounce the character
    character_rect.x += int(dx * bounce_distance)
    character_rect.y += int(dy * bounce_distance)

def main_menu():
    # Load images
    menu_img = pygame.image.load('menu.png').convert_alpha()
    play_img = pygame.image.load('play.png').convert_alpha()
    quit_img = pygame.image.load('quit.png').convert_alpha()

    menu_img = pygame.transform.scale(menu_img, (WIDTH, HEIGHT))
    play_img = pygame.transform.scale(play_img, (200, 80))
    quit_img = pygame.transform.scale(quit_img, (200, 80))

    play_rect = play_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    quit_rect = quit_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    while True:
        screen.blit(menu_img, (0, 0))
        screen.blit(play_img, play_rect)
        screen.blit(quit_img, quit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return  # Start the game
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

def display_winning_page():
    win1_img = pygame.image.load('win1.png').convert_alpha()
    win2_img = pygame.image.load('win2.png').convert_alpha()
    
    win1_img = pygame.transform.scale(win1_img, (WIDTH, HEIGHT))
    win2_img = pygame.transform.scale(win2_img, (WIDTH, HEIGHT))

    screen.blit(win1_img, (0, 0))
    screen.blit(win2_img, (0, 0))

    pygame.display.update()
    pygame.time.wait(3000)  # Display for 3 seconds

game_won = False 

def display_game_over_page():
    gameover_img = pygame.image.load('gameover.png').convert_alpha()
    
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    screen.blit(gameover_img, (0, 0))

    pygame.display.update()
    pygame.time.wait(3000)  # Display for 3 seconds

main_menu()
# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for slider in sliders:
            slider.handle_event(event)

    keys = pygame.key.get_pressed()
    move_direction = (0, 0)  # Initialize movement direction

    if not game_over:
        # Determine movement direction
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_direction = (move_direction[0], -move_speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_direction = (move_direction[0], move_speed)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_direction = (-move_speed, move_direction[1])
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_direction = (move_speed, move_direction[1])

        # Update character's rect position based on movement direction
        character_rect.move_ip(move_direction)

        # Clamp character's rect within screen boundaries
        character_rect.clamp_ip(pygame.Rect(-50, TOP_HEIGHT, WIDTH + 115, HEIGHT - TOP_HEIGHT))

        # Determine the direction the character is facing
        if move_direction[1] < 0:
            if move_direction[0] == 0:
                character_image = direction_images["north"]
            elif move_direction[0] < 0:
                character_image = direction_images["northwest"]
            else:
                character_image = direction_images["northeast"]
        elif move_direction[1] > 0:
            if move_direction[0] == 0:
                character_image = direction_images["south"]
            elif move_direction[0] < 0:
                character_image = direction_images["southwest"]
            else:
                character_image = direction_images["southeast"]
        elif move_direction[0] < 0:
            character_image = direction_images["west"]
        elif move_direction[0] > 0:
            character_image = direction_images["east"]
        else:
            character_image = direction_images["stationary"]

        # Get values from sliders
        radius = radius_slider.get_value()
        speed = speed_slider.get_value()
        weight = weight_slider.get_value()

        radius_scale = 40
        speed_scale = 100
        weight_scale = 1

        ball_size = int(weight * initial_ball_size)

        # Update sliders to reset tangential acceleration if needed
        for slider in sliders:
            slider.update()

        # Calculate centripetal acceleration, centripetal force, and angular velocity
        centripetal_acc = calculate_centripetal_acceleration(radius / radius_scale, speed * speed_scale)
        tangential_acc = speed_slider.get_tangential_acc()
        centripetal_force = calculate_centripetal_force(weight * weight_scale, radius / radius_scale, speed * speed_scale)
        angular_velocity = calculate_angular_velocity(speed * speed_scale, radius / radius_scale)
        angular_acc = calculate_angular_acc(tangential_acc, radius/radius_scale)
        net_force = calculate_net_force(weight * weight_scale, tangential_acc, centripetal_acc)

        # Update output box texts
        angular_velocity_output.update("Angular Velocity: {:.2f} rad/s".format(angular_velocity))
        centripetal_acc_output.update("Centripetal Acc: {:.2f} m/s^2".format(centripetal_acc))
        centripetal_force_output.update("Centripetal Force: {:.2f} N".format(centripetal_force))

        angular_acc_output.update("Angular Acceleration: {:.2f} rad/s^2".format(angular_acc))
        tangential_acc_output.update("Tangential Acceleration: {:.2f} m/s^2".format(tangential_acc))
        net_force_output.update("Net Force: {:.2f} N".format(net_force))


        # Update the position of each zombie to move towards the player
        for zombie_info in zombies:
            zombie_rect = zombie_info['rect']
            dx = character_rect.x - zombie_rect.x
            dy = character_rect.y - zombie_rect.y
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance
            
            # Adjust the direction vector to always point towards the player
            dx *= zombie_speed 
            dy *= zombie_speed 

            # Determine the direction of the zombie
            if abs(dx) > abs(dy):
                if dx > 0:
                    zombie_info['direction'] = 'right'
                else:
                    zombie_info['direction'] = 'left'
            else:
                if dy > 0:
                    zombie_info['direction'] = 'front'
                else:
                    zombie_info['direction'] = 'back'

            # Add a small random component to avoid perfect diagonals
            epsilon = 0.1
            if dx == 0:
                dx += epsilon
            if dy == 0:
                dy += epsilon
            dx += random.uniform(-epsilon, epsilon)
            dy += random.uniform(-epsilon, epsilon)

            # Calculate offset to prevent clustering
            offset_x, offset_y = calculate_offset(zombie_info, zombies)
            dx += offset_x
            dy += offset_y

            zombie_rect.x += dx
            zombie_rect.y += dy

            # Check for collision with the ball
            if ball_rect.colliderect(zombie_rect):
                # Collision detected, bounce the zombie away from the ball
                bounce_away_from_ball(zombie_rect, ball_rect)
                # Skip the rest of the loop iteration to prevent additional movement
                continue

            if character_rect.colliderect(zombie_rect):
                handle_damage()
                
        for zombie_info in zombies:
            zombie_rect = zombie_info['rect']
            zombie_health = zombie_info['health']

            # Calculate circle position
            circle_x = center_x + radius * math.cos(angle)
            circle_y = center_y + radius * math.sin(angle)


            # Update the position of ball_rect
            ball_rect.x = circle_x - ball_rect.width // 2
            ball_rect.y = circle_y - ball_rect.height // 2

            
            if ball_rect.colliderect(zombie_rect):
                # Collision detected, decrease zombie's health
                if centripetal_force <= zombie_info['max_health']:
                    zombie_info['health'] -= int(centripetal_force) # Adjust the amount of damage as needed

                # If the zombie's health is 0 or less, remove it
                if zombie_info['health'] <= 0:
                    zombies.remove(zombie_info)

        # Check if all zombies are eliminated
        if not zombies:
            level += 1
            if level <= 3:
                # Generate zombies for the next level
                zombies = create_wave(base_num_zombies * level, zombie_images, zombie2_images, zombie4_images, zombie3_images)
            else:
                # Game is won
                display_winning_page()
                running = False  # End the game loop


    # Clear the screen
    screen.fill(WHITE)

    # Draw background colors for the top and bottom sections
    # Define the rectangular area for the gradient
    gradient_rect = pygame.Rect(0, 0, WIDTH, 150)

    # Draw the sunset gradient within the rectangular area
    for y in range(gradient_rect.height):
        # Interpolate between horizon_color and sky_color based on y coordinate
        color = (
            int(horizon_color[0] + (sky_color[0] - horizon_color[0]) * y / gradient_rect.height),
            int(horizon_color[1] + (sky_color[1] - horizon_color[1]) * y / gradient_rect.height),
            int(horizon_color[2] + (sky_color[2] - horizon_color[2]) * y / gradient_rect.height)
        )
        pygame.draw.line(screen, color, (gradient_rect.left, gradient_rect.top + y),
                         (gradient_rect.right, gradient_rect.top + y))

    # Draw sliders and output boxes
    for slider in sliders:
        draw_label(slider.label, slider.rect.x, slider.rect.y - 20)
        slider.draw(screen)
        # Draw slider values beside sliders
        if slider == radius_slider:
            draw_label("{:.2f}".format(slider.get_value() / radius_scale), slider.rect.x + slider.rect.width + 10,
                       slider.rect.y)
        elif slider == speed_slider:
            draw_label("{:.2f}".format(slider.get_value() * speed_scale), slider.rect.x + slider.rect.width + 10,
                       slider.rect.y)
        else:
            draw_label("{:.2f}".format(slider.get_value()), slider.rect.x + slider.rect.width + 10, slider.rect.y)

    # Update angle and draw the scene
    angle += speed
    draw_scene(radius, angle, character_rect.centerx, character_rect.centery, ball_image, ball_rect, character_image)

    # Draw health bar above the character
    health_bar_width = int((current_health / MAX_HEALTH) * 100)  # Calculate health bar width
    health_bar_rect = pygame.Rect(character_rect.left, character_rect.top - 20, 100, 10)  # Position the health bar above the character
    pygame.draw.rect(screen, (255, 0, 0), (health_bar_rect.left, health_bar_rect.top, 100, 10))  # Draw red background for health bar
    pygame.draw.rect(screen, (0, 255, 0), (health_bar_rect.left, health_bar_rect.top, health_bar_width, 10))  # Draw green health bar


    # Draw lives display
    for i in range(current_lives):
        screen.blit(heart_image, (i * 30 + 5, 150))

    draw_label("Uniform Circular Motion", 20, 20)
    draw_label("Non-uniform Circular Motion", 530, 20)

    # Draw output boxes
    for output_box in output_boxes:
        output_box.draw(screen)

    # Draw each zombie with health bar
    for zombie_info in zombies:
        zombie_rect = zombie_info['rect']
        zombie_health = zombie_info['health']
        max_health = zombie_info['max_health']
            
        # Draw number of health and damage
        health_text = font.render(f'{zombie_health}/{max_health}', True, (255, 255, 255))
        screen.blit(health_text, (zombie_rect.x + 45, zombie_rect.y - 5))

        # Draw zombie
        zombie_image = get_zombie_image(zombie_info, frame_count)
        screen.blit(zombie_image, zombie_rect)

    # If game over, display a game over message
    if game_over:
        display_game_over_page()
    

    # Update the display
    pygame.display.flip()
    frame_count += 1

    # Cap the frame rate
    clock.tick(75)

pygame.quit()


