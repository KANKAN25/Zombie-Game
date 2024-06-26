import pygame
import math

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

# Main game loop
running = True
clock = pygame.time.Clock()
angle = 0
radius = default_radius
speed = default_speed
weight = default_weight

# Create sliders
radius_slider = Slider(360, 50, 300, 10, 200, default_radius, "Radius (m):")
speed_slider = Slider(360, 90, 300, 0.01, 0.2, default_speed, "Tangential velocity (m/s):")
weight_slider = Slider(360, 130, 300, 0.5, 5.0, default_weight, "Weight (kg):")

sliders = [radius_slider, speed_slider, weight_slider]

# Create output boxes
output_box_height = 20
centripetal_acc_output = OutputBox(50, 20, 250, output_box_height, "Centripetal Acceleration (m/s^2): ")
tangential_acc_output = OutputBox(50, 50, 250, output_box_height, "Tangential Acceleration (m/s^2): ")
centripetal_force_output = OutputBox(50, 110, 250, output_box_height, "Centripetal Force (N): ")
angular_velocity_output = OutputBox(50, 80, 250, output_box_height, "Angular Velocity (rad/s): ")

output_boxes = [centripetal_acc_output, tangential_acc_output, centripetal_force_output, angular_velocity_output]

# Load the background image for the bottom section
background_bottom_image = pygame.image.load("background_bottom.png").convert()
background_bottom_image = pygame.transform.scale(background_bottom_image, (WIDTH, BOTTOM_HEIGHT))

# Load the images for character directions
direction_images = {
    "stationary": pygame.image.load("main_stationary.png").convert,
    "north": pygame.image.load("main_moving_north.png"),
    "south": pygame.image.load("main_moving_south.png"),
    "east": pygame.image.load("main_moving_east.png"),
    "west": pygame.image.load("main_moving_west.png"),
    "northeast": pygame.image.load("main_moving_northeast.png"),
    "northwest": pygame.image.load("main_moving_northwest.png"),
    "southeast": pygame.image.load("main_moving_southeast.png"),
    "southwest": pygame.image.load("main_moving_southwest.png")
}

# Scale all direction images to the same size as the stationary image
scale_factor = 0.3
stationary_image = pygame.transform.scale(direction_images["stationary"], (int(direction_images["stationary"].get_width() * scale_factor), int(direction_images["stationary"].get_height() * scale_factor)))

for key in direction_images:
    direction_images[key] = pygame.transform.scale(direction_images[key], (stationary_image.get_width(), stationary_image.get_height()))

# Define column widths
COLUMN_WIDTH = WIDTH // 3

# Create and position sliders
radius_slider = Slider(COLUMN_WIDTH + 60, 40, 200, 10, 200, default_radius, "Radius:")
speed_slider = Slider(COLUMN_WIDTH + 60, 80, 200, 0.01, 0.2, default_speed, "Speed:")
weight_slider = Slider(COLUMN_WIDTH + 60, 120, 200, 0.5, 5.0, default_weight, "Weight (kg):")

# Create and position output boxes
output_box_height = 20
centripetal_acc_output = OutputBox(50, 20, 250, output_box_height, "Centripetal Acceleration: ")
tangential_acc_output = OutputBox(50, 50, 250, output_box_height, "Tangential Acceleration: ")
angular_velocity_output = OutputBox(50, 80, 250, output_box_height, "Angular Velocity: ")
centripetal_force_output = OutputBox(50, 110, 250, output_box_height, "Centripetal Force: ")

sliders = [radius_slider, speed_slider, weight_slider]
output_boxes = [centripetal_acc_output, tangential_acc_output, angular_velocity_output, centripetal_force_output]

# Define initial position and size of the character's rect
character_rect = stationary_image.get_rect(center=(center_x, center_y))

# Load the image for the ball
ball_image = pygame.image.load("ball.png")

# Define the initial size of the ball
initial_ball_size = 50

# Create a rect for the ball image and scale it
ball_rect = pygame.Rect(0, 0, initial_ball_size, initial_ball_size)
ball_image = pygame.transform.scale(ball_image, (initial_ball_size, initial_ball_size))

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for slider in sliders:
            slider.handle_event(event)

    keys = pygame.key.get_pressed()
    move_direction = (0, 0)  # Initialize movement direction

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
    character_rect.clamp_ip(pygame.Rect(-50, TOP_HEIGHT - 60, WIDTH + 115, HEIGHT - TOP_HEIGHT + 115))

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

    ball_size = int(weight * initial_ball_size)  # Scale the size of the ball based on weight

    # Update sliders to reset tangential acceleration if needed
    for slider in sliders:
        slider.update()

    # Calculate centripetal acceleration, centripetal force, and angular velocity
    centripetal_acc = calculate_centripetal_acceleration(radius / radius_scale, speed * speed_scale)
    tangential_acc = speed_slider.get_tangential_acc()
    centripetal_force = calculate_centripetal_force(weight * weight_scale, radius / radius_scale, speed * speed_scale)
    angular_velocity = calculate_angular_velocity(speed * speed_scale, radius / radius_scale)

    # Update output box texts
    centripetal_acc_output.update("Centripetal Acc: {:.2f} m/s^2".format(centripetal_acc))
    tangential_acc_output.update("Tangential Acc: {:.2f} m/s^2".format(tangential_acc))
    centripetal_force_output.update("Centripetal Force: {:.2f} N".format(centripetal_force))
    angular_velocity_output.update("Angular Velocity: {:.2f} rad/s".format(angular_velocity))


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

    # Draw character image based on rect position
    screen.blit(character_image, character_rect)

    # Update angle and draw the scene
    angle += speed
    draw_scene(radius, angle, character_rect.centerx, character_rect.centery, ball_image, ball_rect, character_image)

    # Draw health bar on top of the character
    #draw_health_bar(screen, center_x, center_y - 30, current_health, MAX_HEALTH)

    # Draw output boxes
    for output_box in output_boxes:
        output_box.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

