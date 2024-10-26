import pygame
import math
from pygame import mixer
import random
from random import randint

pygame.init()

screen = pygame.display.set_mode((800, 600))

with open('highscore.txt', 'r+') as f:
    fscore = f.read()

# space bg
bg = pygame.image.load('./images/space_bg.jpg')

# background music
mixer.music.load('./sounds/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./images/space-invaders.png')
pygame.display.set_icon(icon)



# Player
Playerimg = pygame.image.load('./images/space-invaders.png')
playx = 360
playy = 500
play_change = 0

# Pause Button
pause_button = pygame.image.load('./images/pause_button.png')
pause_rect = pause_button.get_rect()
pause_rect.topleft = (730,10)

# Resume Button
resume_button = pygame.image.load('./images/resume_button.png')
resume_rect = pause_button.get_rect()
resume_rect.topleft = (730,10)

# Score
score_value = 0
font = pygame.font.Font("./fonts/Super Bubble.ttf", 32)
textx = 10
texty = 10


def show_score(textx, texty):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (textx, texty))


def Player(playx, playy):
    screen.blit(Playerimg, (playx, playy))


# enemy images
enemyLoadImg = ['./images/ego_skull.png', './images/stress_skull.png', './images/anger_skull.png', './images/hatred_skull.png', './images/fear_skull.png',
                './images/envy_skull.png']

enemyLoadDict = {}
for img in enemyLoadImg:
    enemyLoadDict[img] = pygame.image.load(img)

enemyImg = []
enemyx = []
enemyy = []
enemy_change_x = []
enemy_change_y = []

no_of_enemies = 4
currentEnemyFiles = random.sample(enemyLoadImg, no_of_enemies)
for i in range(no_of_enemies):
    enemyImg.append(enemyLoadDict[currentEnemyFiles[i]])
    enemyx.append(randint(0, 736))
    enemyy.append(randint(0, 50))
    enemy_change_x.append(0.2)
    enemy_change_y.append(10)


def Enemy(enemyx, enemyy, i):
    screen.blit(enemyImg[i], (enemyx, enemyy))



# bullets
bullx = playx + 16
bully = playy - 10
bullets = pygame.image.load('./images/bullet.png')
bullet_state = "ready"

def bullet(bullx, bully):
    global bullet_state
    screen.blit(bullets, (bullx, bully))
    bullet_state = "fire"


def isCollision(enemyx, enemyy, bullx, bully):
    dis = math.sqrt(pow(enemyx - bullx, 2) + pow(enemyy - bully, 2))
    return dis < 27

def replace_enemy(i):
    global enemyImg, currentEnemyFiles
    collided_enemy_file = currentEnemyFiles[i]

    currentEnemyFiles.pop(i)
    enemyImg.pop(i)

    remainingImages = list(set(enemyLoadImg) - set(currentEnemyFiles))
    new_enemy_file = random.choice(remainingImages)

    currentEnemyFiles.insert(i, new_enemy_file)
    enemyImg.insert(i, enemyLoadDict[new_enemy_file])

    enemyx[i] = randint(0, 736)
    enemyy[i] = randint(0, 50)


font1 = pygame.font.Font("./fonts/Super Bubble.ttf", 72)
font2 = pygame.font.Font("./fonts/Super Bubble.ttf", 60)
overx = 160
overy = 250
hsx =60
hsy=250

def game_over_text():
    over = font1.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (overx, overy))

def checkNewHighScore(score):
    if int(fscore) < int(score):
        return True
    else:
        return False
def new_high_score_text(score):
    hs = font2.render('New High Score:\n' + str(score), True, (255, 255, 255))
    screen.blit(hs,(hsx,hsy))





# game loop
running = True
Is_paused = False
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not Is_paused and pause_rect.collidepoint(event.pos):
                Is_paused = True
            elif Is_paused and resume_rect.collidepoint(event.pos):
                Is_paused = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                play_change = -2
            if event.key == pygame.K_RIGHT:
                play_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("./sounds/laser.wav")
                    bulletSound.play()
                    bullx = playx + 16
                    bullet_state = "fire"

        if event.type == pygame.KEYUP:
            play_change = 0

    if Is_paused == False:
        playx += play_change

    if playx <= 0:
        playx = 10
    if playx >= 734:
        playx = 700

    for i in range(no_of_enemies):
        if enemyy[i] >= 400:
            for j in range(no_of_enemies):
                enemyy[j] = 2000

            Is_high_score = checkNewHighScore(score_value)
            if Is_high_score:
                new_high_score_text(score_value)
                break
            else:
                game_over_text()
                break



        if Is_paused == False:
            screen.blit(pause_button, pause_rect.topleft)
            # pause_the_game()

            enemyx[i] += enemy_change_x[i]
            if enemyx[i] <= 0:
                enemy_change_x[i] = 0.3
                enemyy[i] += enemy_change_y[i]
            if enemyx[i] >= 700:
                enemy_change_x[i] = -3  # to be changed
                enemyy[i] += enemy_change_y[i]
            if bully <= 0:
                bully = playy - 10
                bullet_state = 'ready'
            if bullet_state == "fire":
                bullet(bullx, bully)
                bully -= 5
        if Is_paused == True:
            screen.blit(resume_button, resume_rect.topleft)





        # Collision Checking
        collision = isCollision(enemyx[i], enemyy[i], bullx, bully)
        if collision:
            explosionSound = mixer.Sound("./sounds/explosion.wav")
            explosionSound.play()
            score_value += 1
            bullet_state = "ready"

            # Replace enemy after collision
            replace_enemy(i)

            bullx = playx + 16
            bully = playy - 10
            if int(fscore) < score_value:
                with open('highscore.txt', 'w') as f1:
                    f1.write(str(score_value))

        Enemy(enemyx[i], enemyy[i], i)

    Player(playx, playy)
    show_score(textx, texty)

    pygame.display.update()

pygame.quit()
