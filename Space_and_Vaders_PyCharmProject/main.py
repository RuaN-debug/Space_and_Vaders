import pygame
import math
import random
from pygame import mixer

# Initialization
pygame.init()

# Screen Creation
screen = pygame.display.set_mode((800, 600))

# Framerate cap
clock = pygame.time.Clock()

# Background
background = pygame.image.load('Images/background.png').convert_alpha()

mixer.music.load('Sounds/background.wav')
mixer.music.set_volume(0.03)
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space and Vaders")
icon = pygame.image.load('Images/spaceship.png').convert_alpha()
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Images/player.png').convert_alpha()
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemiesQuantity = 6

for i in range(enemiesQuantity):
    enemyImg.append(pygame.image.load('Images/vader.png').convert_alpha())
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('Images/bullet.png').convert_alpha()
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_fired = False

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_test = False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (200, 250))
    mixer.music.fadeout(2000)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_fired
    bullet_fired = True
    screen.blit(bulletImg, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27


# Game Loop
running = True
test = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checks if any key is pressed and which key it is
        if event.type == pygame.KEYDOWN and not game_over_test:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE and bullet_fired is False:
                bullet_sound = mixer.Sound('Sounds/laser.wav')
                bullet_sound.set_volume(0.04)
                bullet_sound.play()

                bulletX = playerX
                bullet_fire(bulletX, bulletY)

    # Boundaries for the player on the screen
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Boundaries for the enemies on the screen
    for i in range(enemiesQuantity):
        # Game Over
        if enemyY[i] > 440:
            for j in range(enemiesQuantity):
                enemyY[j] = 1000
            game_over()
            game_over_test = True
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision_test = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision_test:
            explosion_sound = mixer.Sound('Sounds/explosion.wav')
            explosion_sound.set_volume(0.02)
            explosion_sound.play()

            bulletY = 480
            bullet_fired = False
            score_value += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_fired = False

    if bullet_fired is True:
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    clock.tick(60)
