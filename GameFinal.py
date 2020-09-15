import pygame
import random
from math import sqrt
import time
from pygame import mixer



#initialise pygame
pygame.init()
clock = pygame.time.Clock()

#define colours
black = (0,0,0)
white = (255,255,255)

#define different font sizes
smallfont = pygame.font.SysFont("comicsansms", 18)
largefont = pygame.font.SysFont("comicsansms", 64)

#Create the screen
screenX = 420
screenY = 600
screen = pygame.display.set_mode((screenX,screenY))

#Title and Icon
pygame.display.set_caption("Infinity War")
icon = pygame.image.load('avengers1.png')
pygame.display.set_icon(icon)

#Score display
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
#coordinates of score text on screen
textX = 10
textY = 10

#Game Over text
over_text = pygame.font.Font('freesansbold.ttf',48)

#enemyfire event, occurs every 10ms
enemy_fire = pygame.USEREVENT
pygame.time.set_timer(enemy_fire,10)

#You win text
win_text = pygame.font.Font('freesansbold.ttf',48)

#Player Image and Position
playerImg = pygame.image.load('ironman1.png')
playerX = screenX/2 - 50
playerY = screenY - 90
#Horizontal movement only
playerX_change = 0

#Multiple Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7
change = 0.15

for i in range(num_of_enemies):
    #Enemy Image and Position (Bonus Enemy included)
    if i==4:
        enemyImg.append(pygame.image.load('thanos.png'))
    
    else:
        enemyImg.append(pygame.image.load('hand.png'))
    #Random appearance on screen
    enemyX.append(random.randint(0,screenX-64))
    enemyY.append(random.randint(20,100))
    #Horizontal and Vertical movement
    enemyX_change.append(0.1)
    enemyY_change.append(30)

#Bullet Image and Position
bulletImg = pygame.image.load('32.png')
bulletX = 0
#Same as player
bulletY = 480
#Vertical movement only
bulletY_change = 0.5
#Ready - can't see bullet on screen, Fire - bullet currently moving
bullet_state = 'ready'

#Enemy Bullet Image and Position, fires randomly from top of screen
enemybulletImg = pygame.image.load('bolt.png')
enemybulletX = random.randint(0,screenX-40)
#Same as player
enemybulletY = 0
#Vertical movement only
enemybulletY_change = 0.2
#Ready - can't see bullet on screen, Fire - bullet currently moving
enemybullet_state = 'ready'


#function to render score text and blit it onto the screen
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255)) 
    screen.blit(score,(x,y))

#function to display 'game over' on middle of screen (250,250)
def game_over():

    gameover = True

    while gameover:
        for event in pygame.event.get():
            #cross exits game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(black)    
        gameover = over_text.render("GAME OVER", True, (255,255,255))
        screen.blit(gameover,(55 ,250)) 
        pygame.display.update()
    
        
#function to display 'you win' on middle of screen (250,250)
def win_game():

    wingame = True

    while wingame:
        for event in pygame.event.get():
            #cross exits game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
      
        screen.fill(black)
        wingame = win_text.render("YOU WIN!", True, (255,255,255))
        screen.blit(wingame,(90 ,250))
        score = font.render("Score: " + str(score_value), True, (255,255,255)) 
        screen.blit(score,(textX,textY))
        pygame.display.update()
            
#Drawing player on screen
def player(x,y):
    screen.blit(playerImg,(x,y))
    

#Drawing enemy on screen, specifies image from list of enemies
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#Changing state of bullet from ready to fire, blit bullet on to screen
def fire_bullet(x,y):
    #Make bullet_state global so it can be called inside the function
    #Runs when spacebar is pressed
    global bullet_state
    bullet_state = "fire"
    #positions bullet front and central of character
    screen.blit(bulletImg,(x+25,y+17))
                
#enemy bullet - changing state of enemy bullet from ready to fire, blit enemy bullet on to screen
def enemyfire_bullet(x,y):
    #Make bullet_state global so it can be called inside the function
    global enemybullet_state
    enemybullet_state = "fire"
    #positions bullet front and central of character
    screen.blit(enemybulletImg,(int(x)+17,int(y)+50))

#Calcuate distance between enemy and bullet using mathematical formula to calculate whether collision has occured  
def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = sqrt(pow(enemyX-bulletX,2) + pow(enemyY-bulletY,2))
    #25 by trial and error, if collision occurs, return True
    if distance < 25:
        return True
    else:
        return False

#Calcuate distance between player and enemy bullet using mathematical formula to calculate whether collision has occured  
def playeriscollision(playerX,playerY,enemybulletX,enemybulletY):
    #Calcuate distance between enemy and bullet using mathematical formula
    distance = sqrt(pow(playerX-enemybulletX,2) + pow(playerY-enemybulletY,2))
    #27 by trial and error, if collision occurs, return True
    if distance < 27:
        return True
    else:
        return False

#Game intro code
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #cross exits game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #press p for play or q for quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        #displays text on game intro screen          
        screen.fill(black)
        message_to_screen("Infinity War",
                          (0,0,255),
                          -250,
                          "large")
        message_to_screen("You must defeat Thanos and his infinity stones!",
                          (255,211,3),
                          -150)

        message_to_screen("Score 300 POINTS before Thanos and",
                          (252,127,3),
                          -100)

        message_to_screen("his infinity stones reach Earth!",
                          (252,127,3),
                          -70)

        message_to_screen("They speed up after you reach 150 POINTS!",
                          (252,127,3),
                          -40)

        message_to_screen("Press SPACEBAR to fire repulsor blasts",
                          (0,255,0),
                          0)

        message_to_screen("Blasting the infinity stones = 5 points",
                          (0,255,0),
                          40)

        message_to_screen("Blasting Thanos = 20 points",
                          (0,255,0),
                          80)

        message_to_screen("Avoid the falling energy beams",
                          (255,0,0),
                          120)

        message_to_screen("or you will lose 20 points!",
                          (255,0,0),
                          150)

        message_to_screen("Press P to play or Q to quit.",
                          (252,3,202),
                          250)

        pygame.display.update()

        
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()
    
#define text, colour, position relative to centre of screen and size of text    
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (screenX/2),(screenY/2)+y_displace
    screen.blit(textSurf,textRect)


#Run game intro function to get game intro screen
game_intro()

           
#Game Loop - anything that has to persist will be in the while loop
running = True
#Background Music
mixer.music.load('Music.mp3')
mixer.music.play(-1)
while running:
    #RGB - RED, Green, Blue
    screen.fill(black)
    
    #Background image constantly running, drawn from (0,0)
    #screen.blit(background,(0,0))
    #Draw enemy boundary line on screen
    pygame.draw.rect(screen,(255,255,255),[0,490,420,1])
   
                     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        #Check for any keystroke
        #key pressed
        if event.type == pygame.KEYDOWN:
            #Check if pressed key is left or right
            if event.key == pygame.K_LEFT:
                #Horizontal movement left
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                #Horizontal movement right
                playerX_change = 0.4
            #Fire bullet when spacebar pressed
            if event.key == pygame.K_SPACE:
                #Only fire bullet once the previous bullet has gone above 0 co-ord (in ready condition)
                if bullet_state == 'ready':
                    #bullet sound
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                #Save position of where bullet was fired from (x-coord)
                    bulletX = playerX
                #fire_bullet called with current position of where bullet was fired from
                    fire_bullet(bulletX,bulletY)
                    
        #key released - no player movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        #run timed event - fires enemy bullet from a random point at the top of the screen
        if event.type == enemy_fire:
            if enemybullet_state == 'ready':
                enemybulletX = random.randint(-15,screenX-35)
                enemybulletY = 0
                enemyfire_bullet(enemybulletX,enemybulletY)
                             
    #Old playerX position + new position(depends on which key pressed)        
    playerX += playerX_change
   
    #restricting player boundaries so icon doesn't go out of bounds - positions player back in boundary
    if playerX < -15:
        playerX = -15   
    elif playerX > screenX - 70:
        playerX = screenX - 70



    #All enemy related activities in for loop
    #Enemy movement
    #As there are multiple enemies, need to specify which one to move
    for i in range(num_of_enemies):
        #Game Over - if any enemy reaches boundary, they will be moved off the screen and it will be game over      
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000     
            #stop background music and play victory sound
            mixer.music.stop()
            explosion_Sound = mixer.Sound('Bomb.wav')
            explosion_Sound.play()
            time.sleep(1)
            bullet_Sound = mixer.Sound('loss.wav')
            bullet_Sound.play()
            running = False
            game_over()
            
            
        #Display win game screen if you score 300+ points
        if score_value >= 300:
            #stop background music and play victory sound
            mixer.music.stop()
            time.sleep(1)
            bullet_Sound = mixer.Sound('victory.wav')
            bullet_Sound.play()
            running = False
            win_game()
            
            
        
        #restricting enemy boundaries so icon doesn't go out of bounds
        #Changing direction and speed(increases after 150 points) and moving enemy down when it hits boundary        
        if enemyX[i] < -14:
            if score_value <= 150:
                enemyX_change[i] = change
                
            else:
                enemyX_change[i] = change*2               
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] > screenX - 45:
            if score_value <= 150:
                enemyX_change[i] = change*-1
            
            else:
                enemyX_change[i] = change*(-2)
            enemyY[i] += enemyY_change[i]
        
        #continuously changes enemy's x position
        enemyX[i] += enemyX_change[i]


        #Collision
        #Stores true or false depending on result of function
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        #if true  
        if collision:
            #explosion sound when collision occurs
            explosion_Sound = mixer.Sound('Bomb.wav')
            explosion_Sound.play()

            #reset bullet to starting position, add 5/20 to score depending on who is shot, enemy respawns from random position
            bulletY = 480
            bullet_state = 'ready'
            if i==4:        
                score_value += 20
                              
            else:         
                score_value += 5
                                
            enemyX[i] = random.randint(0,screenX-64)
            enemyY[i] = random.randint(20,100)

        #specify enemy for enemy function - respawning
        enemy(enemyX[i],enemyY[i],i)


    playercollision = playeriscollision(playerX,playerY,enemybulletX,enemybulletY)
    #if true         
    if playercollision:
    #reset bullet to starting position, subtract 20 from score, enemy respawns from random position
        explosion_Sound = mixer.Sound('Bomb.wav')
        explosion_Sound.play()
        enemybulletX = random.randint(-15,screenX-40)
        enemybulletY = 0
        score_value -= 20
                              

    #Bullet Movement
    #resets bullet to starting point(ready) if it goes off the screen
    if bulletY < 0:
        bulletY = 480
        bullet_state = 'ready'
    #fires bullet vertically   
    if bullet_state == "fire":       
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    
    #reset enemy bullet if it reaches off screen
    if enemybulletY > 550:
        enemybullet_state = 'ready'   
    #fires bullet vertically   
    if enemybullet_state=='fire':
        enemyfire_bullet(enemybulletX,enemybulletY)
        enemybulletY += enemybulletY_change
        
    #Player's position
    player(playerX,playerY)
    #Display the score
    show_score(textX,textY)

    pygame.display.update()
