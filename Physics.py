import pygame
import random
import math

def create_wave(num_zombies, zombie_image, zombie_image_2, zombie_image_3):
    zombies = []
    for _ in range(num_zombies):
        zombie_rect = zombie_image.get_rect()
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

        # Randomly select one of the zombie images and set health accordingly
        zombie_image_choice = random.choice([(zombie_image, 25), (zombie_image_2, 40), (zombie_image_3, 65)])
        chosen_image, health = zombie_image_choice

        zombies.append({'rect': zombie_rect, 'health': health, 'max_health': health, 'image': chosen_image})  # Add health and image to each zombie
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

# Load images
zombie_image = pygame.image.load(r'C:\Users\hp\OneDrive\Documents\cmsc21\Pygame\Zombies\graphics\nicole.png').convert_alpha()
zombie_image_2 = pygame.image.load(r'C:\Users\hp\OneDrive\Documents\cmsc21\Pygame\Zombies\graphics\nicole2.png').convert_alpha()
zombie_image_3 = pygame.image.load(r'C:\Users\hp\OneDrive\Documents\cmsc21\Pygame\Zombies\graphics\nicole3.png').convert_alpha()
player_image = pygame.image.load(r'C:\Users\hp\OneDrive\Documents\cmsc21\Pygame\Zombies\graphics\user.png').convert_alpha()

# Scale images
zombie_image = pygame.transform.scale(zombie_image, (40, 40))  # Adjust size as needed
zombie_image_2 = pygame.transform.scale(zombie_image_2, (40, 40))  # Adjust size as needed
zombie_image_3 = pygame.transform.scale(zombie_image_3, (40, 40))  # Adjust size as needed
player_image = pygame.transform.scale(player_image, (40, 40))  # Adjust size as needed

# Create player
player_rect = player_image.get_rect()
player_rect.center = (400, 200)  # Start at the center of the screen

# Game state variables
level = 1
base_num_zombies = 5  # Base number of zombies for level 1
zombies = create_wave(base_num_zombies * level, zombie_image, zombie_image_2, zombie_image_3)

# Main game loop
running = True
clock = pygame.time.Clock()
player_speed = 2.3  # Speed of the player
zombie_speed_factor = 0.7  # Factor to reduce zombie speed

# Game over flag
game_over = False

# Fonts
font = pygame.font.Font(None, 18)

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
            dx *= zombie_speed_factor
            dy *= zombie_speed_factor

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
            zombies = create_wave(base_num_zombies * level, zombie_image, zombie_image_2, zombie_image_3)

    # Clear the screen
    screen.fill((30, 30, 30))

    # Draw the player
    screen.blit(player_image, player_rect)

    # Draw each zombie with health bar
    for zombie_info in zombies:
        zombie_rect = zombie_info['rect']
        zombie_health = zombie_info['health']
        max_health = zombie_info['max_health']
        zombie_image = zombie_info['image']  # Get the zombie image
        
        # Draw health bar
        bar_width = 40  # Width of the health bar
        health_bar_width = int((zombie_health / max_health) * bar_width)  # Calculate the width based on health percentage
        pygame.draw.rect(screen, (255, 0, 0), (zombie_rect.x, zombie_rect.y - 5, bar_width, 3))  # Red bar
        pygame.draw.rect(screen, (0, 255, 0), (zombie_rect.x, zombie_rect.y - 5, health_bar_width, 3))  # Green bar based on health

        
        # Draw number of health and damage
        health_text = font.render(f'{zombie_health}/{max_health}', True, (255, 255, 255))
        screen.blit(health_text, (zombie_rect.x + 45, zombie_rect.y - 5))

        # Draw zombie
        screen.blit(zombie_image, zombie_rect)

    # If game over, display a game over message
    if game_over:
        font = pygame.font.Font(None, 24)
        text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(text, (250, 150))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
