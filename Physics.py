import pygame
import random
import math

def create_wave(num_zombies, zombie_images, zombie_images_2, zombie_images_4, zombie_images_3):
    zombies = []
    directions = ['front', 'back', 'left', 'right']
    for _ in range(num_zombies):
        zombie_rect = zombie_images['front'][0].get_rect()
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            zombie_rect.x = random.randint(0, 800)
            zombie_rect.y = -50
        elif edge == 'bottom':
            zombie_rect.x = random.randint(0, 800)
            zombie_rect.y = 450
        elif edge == 'left':
            zombie_rect.x = -50
            zombie_rect.y = random.randint(0, 400)
        elif edge == 'right':
            zombie_rect.x = 850
            zombie_rect.y = random.randint(0, 400)

        zombie_image_choice = random.choice([(zombie_images, 25), (zombie_images_2, 40), (zombie_images_4, 50), (zombie_images_3, 65)])
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

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Zombie Wave")

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

player_image = pygame.image.load('user.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (40, 40))

# Create player
player_rect = player_image.get_rect()
player_rect.center = (400, 200)  # Start at the center of the screen

# Game state variables
level = 1
base_num_zombies = 5  # Base number of zombies
zombies = create_wave(base_num_zombies * level, zombie_images, zombie2_images, zombie4_images, zombie3_images)

# Main game loop
running = True
clock = pygame.time.Clock()
player_speed = 1.3  # Speed of the player
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Get keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_d]:
            player_rect.x += player_speed
        if keys[pygame.K_w]:
            player_rect.y -= player_speed
        if keys[pygame.K_s]:
            player_rect.y += player_speed

        # Boundary checks for the player
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > 800:
            player_rect.right = 800
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > 400:
            player_rect.bottom = 400

        # Update the position of each zombie to move towards the player
        for zombie_info in zombies:
            zombie_rect = zombie_info['rect']
            dx = player_rect.x - zombie_rect.x
            dy = player_rect.y - zombie_rect.y
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

            # Check for collision with the player
            if zombie_rect.colliderect(player_rect):
                game_over = True
                break

        # Check if all zombies are eliminated
        if all(zombie['health'] <= 0 for zombie in zombies):
            level += 1
            zombies = create_wave(base_num_zombies * level, zombie_images, zombie2_images, zombie3_images)

    # Clear the screen
    screen.fill((30, 30, 30))

    # Draw the player
    screen.blit(player_image, player_rect)

    # Draw each zombie with health bar
    for zombie_info in zombies:
        zombie_rect = zombie_info['rect']
        zombie_health = zombie_info['health']
        max_health = zombie_info['max_health']
        
        # Draw health bar
        bar_width = 40  # Width of the health bar
        health_bar_width = int((zombie_health / max_health) * bar_width)  # Calculate the width based on health percentage
        pygame.draw.rect(screen, (255, 0, 0), (zombie_rect.x, zombie_rect.y - 5, bar_width, 3))  # Red bar for damage
        pygame.draw.rect(screen, (0, 255, 0), (zombie_rect.x, zombie_rect.y - 5, health_bar_width, 3))  # Green bar for health

        # Draw number of health and damage
        health_text = font.render(f'{zombie_health}/{max_health}', True, (255, 255, 255))
        screen.blit(health_text, (zombie_rect.x + 45, zombie_rect.y - 5))

        # Draw zombie
        zombie_image = get_zombie_image(zombie_info, frame_count)
        screen.blit(zombie_image, zombie_rect)

    # If game over, display a game over message
    if game_over:
        font = pygame.font.Font(None, 48)
        text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(text, (250, 150))

    # Update the display
    pygame.display.flip()
    frame_count += 1

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
