#coding:utf-8
#coding:latin

# python main.py

# https://fr.freepik.com/
# On télécharge une image et on la réduit à 800x600px

import pygame
import random
import math

# Son
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load('images/red-paint-800-600px.png')

# Backgound Sound
mixer.music.load('sound/background.wav')
mixer.music.play(-1)

# Caption and icon
pygame.display.set_caption("Covid Invaders")

# https://www.flaticon.com/
icon = pygame.image.load("images/covid-19.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("images/seringue2.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("images/virus-64px.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# Score
score_value = 0
# Affichage Ã  l'écran du score
font = pygame.font.Font('police/GAME_glm.ttf', 48)

textX = 10
testY = 10

# Game over text
over_font = pygame.font.Font('police/GAME_glm.ttf', 60)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x - 2, y - 40))

# distance between two points : square root of (x2 - x1)Â² + (y2 - y1)Â²
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # RGB - red, green, blue
    screen.fill((0, 0, 0))
    # playerX += 0.1
    # playerY -= 0.1
    # playerX -= 0.1

    # print(playerX)

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is preased check whether it's right or left
        if event.type == pygame.KEYDOWN:
            # print("A Keystroke is pressed.")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Son tir
                    bullet_Sound = mixer.Sound('sound/laser.wav')
                    bullet_Sound.play()
                    # Get the current x coordonate of the virus
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Checking for boundaries of virus so it doesn't go out of bounds
    playerX += playerX_change

    # Screen border
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440: # si l'ennemi approche de 200px
            for j in range(num_of_enemies):
                enemyY[j] = 2000 # sous l'Ã©cran
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        # Screen border
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Son tir
            explosion_Sound = mixer.Sound('sound/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # L'ennemi est réinitialisé quand il est touché.
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

