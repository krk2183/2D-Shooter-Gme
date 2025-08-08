import pygame
import math
import random

pygame.init()

# General screen settings
WIDTH, HEIGHT = 1000, 800
screen_main = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

# Colors are predefined for easier usage
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0) 
random_colors_list = [RED, GREEN, YELLOW, CYAN, ORANGE] # White isn't included since its player's color

font = pygame.font.SysFont(None, 36)
font2 = pygame.font.SysFont(None, 30)

# Function that displays player score
def display_score(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen_main.blit(text_surface, (x, y))



# Function that displays a list of powers the player has unlocked
def display_powers(text_list, color, x, y):
    y_offset = y
    for text in text_list:
        text_surface = font2.render(text, True, color)
        screen_main.blit(text_surface, (x, y_offset))
        y_offset += 30

# Player configurable files
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 20
CUSTOM_HEALTH = 50
player_health = CUSTOM_HEALTH

# Enemy shooting parameters
ENEMY_SHOOT_DELAY = 1600
ENEMY_SHOOT_AMOUNT = 2
last_enemy_shot_time = pygame.time.get_ticks()

# Player shooting parameters
PLAYER_SHOOT_DELAY = 800  
last_player_shot_time = pygame.time.get_ticks()
is_dual_shot = False
health_per_kill = 0

killcount = 0
kills = 0
enemy_count = 2

# Bullets list
bullets_list = []
enemy_bullets_list = []

# Enemies
enemies_list = []
explosions = []

# Enemy spawner. This function will be used in several if cases
def spawn_enemies(count):
    for _ in range(count):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        enemies_list.append({
            'rect': pygame.Rect(x, y, 30, 30), # Enemy gets a random X and Y location on the screen
            'color': random.choice(random_colors_list) # Enemy gets one of the colors inside the random_colors_list 
        })

spawn_enemies(enemy_count)

clockt = pygame.time.Clock()
round = 0 # Variable that keeps count of the rounds


################################################################################################################################################3
################################################################################################################################################3


running = True
paused = False

while running:
    clockt.tick(60)
    screen_main.fill(BLACK) # Background color
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quits if the event is set to QUIT
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # On button click...
            if current_time - last_player_shot_time > PLAYER_SHOOT_DELAY: # If the shooting time interval has passed
                last_player_shot_time = current_time 
                mouse_x, mouse_y = pygame.mouse.get_pos() # Get the position of the mouse to check if it has touched the enemy
                dx = mouse_x - player_pos[0]
                dy = mouse_y - player_pos[1]
                aci = math.atan2(dy, dx) # Two argument arctangent will be determining which quadrant the player fired in
                speed = 10
                
                # Following function translates the bullet's movement from
                # Polar coordinate to Cartesian coordinate
                bullets_list.append({
                    'x': player_pos[0],
                    'y': player_pos[1],
                    'dx': math.cos(aci) * speed,
                    'dy': math.sin(aci) * speed,
                    'r': 5
                })
                # This one builds upon the same logic but spawns two bullet objects
                if is_dual_shot:
                    bullets_list.append({
                        'x': player_pos[0] + math.cos(aci + math.pi/12) * 20, # This bullet fires slightly
                        'y': player_pos[1] + math.sin(aci + math.pi/12) * 20, # clockwise because of pi/12 which is 15 degrees
                        'dx': math.cos(aci + math.pi/12) * speed, # Delta x
                        'dy': math.sin(aci + math.pi/12) * speed, # Delta y 
                        'r': 5
                    })
                    bullets_list.append({
                        'x': player_pos[0] + math.cos(aci - math.pi/12) * 20, # And the second bullet fires
                        'y': player_pos[1] + math.sin(aci - math.pi/12) * 20, # counterclockwise
                        'dx': math.cos(aci - math.pi/12) * speed,
                        'dy': math.sin(aci - math.pi/12) * speed,
                        'r': 5
                    })

    # Enemy shooting logic 
    if current_time - last_enemy_shot_time > ENEMY_SHOOT_DELAY: # If the enemy shooting interval has passed
        last_enemy_shot_time = current_time # Change last shot time to current game time
        if enemies_list:
            for _ in range(min(len(enemies_list), ENEMY_SHOOT_AMOUNT)): # This limits how many enemies can shoot at once
                enemy_to_shoot = random.choice(enemies_list)
                dx = player_pos[0] - enemy_to_shoot['rect'].centerx 
                dy = player_pos[1] - enemy_to_shoot['rect'].centery
                aci = math.atan2(dy, dx)
                speed = 7
                enemy_bullets_list.append({
                    'x': enemy_to_shoot['rect'].centerx,
                    'y': enemy_to_shoot['rect'].centery,
                    'dx': math.cos(aci) * speed,
                    'dy': math.sin(aci) * speed,
                    'r': 5
                })

    # Draw player
    pygame.draw.circle(screen_main, WHITE, player_pos, player_size)
    display_score(f"Kills:  {kills}", (255, 25, 255), 10, 10) # Render items 'Kills' 'Round' 'Health'
    display_score(f"Round:  {round}", (0, 0, 255), 10, 50)
    display_score(f"Health: {player_health}", YELLOW, 10, 90)
    

    powers_list = ["Powers:"] # Adds powers as the player progresses through rounds
    if round >= 5:
        powers_list.append("  +2 Health per Kill")
    if round >= 10:
        powers_list.append("  Faster Shots (0.4s)")
    if round >= 20:
        powers_list.append("  Triple Shot (0.5s)")
    if round >= 30: 
        powers_list.append("  Rapid Fire (0.05s)") 

    display_powers(powers_list, CYAN, WIDTH - 200, 10)  # Render powers list

    # Update and draw player bullets
    for bullet in bullets_list[:]:
        bullet['x'] += bullet['dx'] # Change location by adding its delta to current location
        bullet['y'] += bullet['dy']
        pygame.draw.circle(screen_main, GREEN, (int(bullet['x']), int(bullet['y'])), bullet['r'])

        if not (0 <= bullet['x'] <= WIDTH and 0 <= bullet['y'] <= HEIGHT): # If out of screen
            bullets_list.remove(bullet)
            continue 

        for enemy in enemies_list[:]:
            if enemy['rect'].collidepoint(bullet['x'], bullet['y']): # If the bullet collides with an object an explosion effect and remove that said object
                # Add explosion effect at enemy's position
                explosions.append({
                    'x': enemy['rect'].centerx,
                    'y': enemy['rect'].centery,
                    'radius': 0,
                    'max_radius': 40, 
                    'life': 0,
                    'max_life': 20,
                    'color': random.choice(random_colors_list) # Assign a color once
                })

                try:
                    enemies_list.remove(enemy)
                    bullets_list.remove(bullet)
                    player_health += health_per_kill # Increase the health of the enemy as its unlocked after round 5
                    killcount += 1
                    kills += 1
                    if killcount >= enemy_count: # This means that if all of the enemies have been killed...
                        round += 1
                        if round % 2 == 0: # After 2 levels increase enemy count
                            enemy_count += 1 
                        if round == 5: # Change player parameters (Giving powers when unlocked)
                            health_per_kill = 2
                        if round == 10:
                            PLAYER_SHOOT_DELAY = 400
                        if round == 20:
                            is_dual_shot = True
                            PLAYER_SHOOT_DELAY = 500
                        if round == 30:
                            is_dual_shot=False 
                            PLAYER_SHOOT_DELAY=50
                        spawn_enemies(enemy_count)
                        killcount = 0
                except ValueError: 
                    pass
                break 

    # Update and draw enemy bullets
    for bullet in enemy_bullets_list[:]:
        bullet['x'] += bullet['dx']
        bullet['y'] += bullet['dy']
        pygame.draw.circle(screen_main, RED, (int(bullet['x']), int(bullet['y'])), bullet['r'])

        if not (0 <= bullet['x'] <= WIDTH and 0 <= bullet['y'] <= HEIGHT): # Same logic as player bullets
            enemy_bullets_list.remove(bullet)
            continue

        player_rect = pygame.Rect(player_pos[0] - player_size, player_pos[1] - player_size, player_size * 2, player_size * 2)
        if player_rect.collidepoint(bullet['x'], bullet['y']):
            enemy_bullets_list.remove(bullet)
            player_health -= 10
            if player_health <= 0:
                running = False
            break

    # Update and draw explosions
    for explosion in explosions[:]:
        explosion['radius'] += explosion['max_radius'] / explosion['max_life'] 
        explosion['life'] += 1
        
        alpha = 255 - int(255 * (explosion['life'] / explosion['max_life'])) # This creates a fading effect 
        if alpha < 0: alpha = 0 
        
        color = explosion['color'] # Use the stored color
        explosion_surface = pygame.Surface((explosion['max_radius'] * 2, explosion['max_radius'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(explosion_surface, (color[0], color[1], color[2], alpha), 
                           (explosion['max_radius'], explosion['max_radius']), int(explosion['radius']))
        
        screen_main.blit(explosion_surface, (explosion['x'] - explosion['max_radius'], explosion['y'] - explosion['max_radius']))

        if explosion['life'] >= explosion['max_life']:
            explosions.remove(explosion)

    # Draw enemies
    for enemy in enemies_list:
        pygame.draw.rect(screen_main, enemy['color'], enemy['rect'])

    pygame.display.flip()

pygame.quit()