import pygame
import random
import math
from pygame import mixer

#pygame ekranini baslatma
pygame.init()

#oyunun sahnesini tasarlama
game_screen = pygame.display.set_mode((1280, 720))

#Oyunun arkaplani
background = pygame.image.load('space.jpg')

#Sesler
mixer.music.load('ambient.mp3')
mixer.music.play(-1)

#oyunun ekranda cikacak title ve iconu
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('spaceship.png')
playerX=700
playerX_change =0
playerY=650

#Alien
#Dusmanlarin turetilmesi icin
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    alienImg.append(pygame.image.load('ufo.png'))
    #alienImg = pygame.image.load('ufo.png')
    alienX.append( random.randint(0, 1270))
    alienX_change.append(8)
    alienY.append(random.randint(50, 200))
    alienY_change.append(4)

#Rocket
rocketImg = pygame.image.load('missile.png')
rocketX= 0
rocketX_change =8
rocketY=650
rocketY_change = 10
rocket_state = "Ready!"

#Skor
score= 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game Over ekrani
over_font= pygame.font.Font('freesansbold.ttf',64)

def scoreShow(x,y):
    score_read= font.render("Score: "+ str(score), True, (50,255,255))
    game_screen.blit(score_read, (x,y))

def gameover_text():
    over_text= over_font.render("VICTORY ", True, (0,255,0))
    game_screen.blit(over_text,(350,350))

def player (x,y):
    game_screen.blit(playerImg, (x, y))
    
def alien (x,y,i):
    game_screen.blit(alienImg[i], (x, y))
    
def fire_rocket(x,y):
    global rocket_state
    rocket_state = "fire"
    game_screen.blit(rocketImg, (x, y))

#Nesnelerin gerekli carpmayi hissetmesi gerekiyor
def Collision(alienX, alienY, rocketX, rocketY):
        distance= math.sqrt((math.pow(alienX - rocketX, 2)) + (math.pow(alienY - rocketY, 2)))
        if distance < 27:
            return True
        else:
            return False

#Oyunun dongusu burada. Eger oyun calisiyorsa, calisirken bir tusa basilmissa tepki goster.
game_working = True
while game_working:
        
    #RGB'ye gore doluyor'
    game_screen.fill((0, 0, 0))
    #Arkaplani ekleme
    game_screen.blit(background, (0,0))
    
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_working = False
            
    #Eger oklara basiliyorsa player calissin
    if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
                 playerX_change = -6.1
          if event.key == pygame.K_RIGHT:
                playerX_change = 6.1
          if event.key == pygame.K_SPACE:
                if rocket_state == "Ready!":
                    rocket_sound = mixer.Sound('laser.mp3')
                    rocket_sound.play()
                    #Oyuncunun X koordinati aliniyor
                    rocketX = playerX
                    fire_rocket(rocketX, rocketY)
              
    if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                  playerX_change = 0
   
   #Oyuncunun hareket etme komutlari
    playerX += playerX_change
    
    #ekrani sinirlandirmak icin yapildi
    if playerX <= 0:
          playerX = 0
    elif playerX >= 1200:
           playerX= 1200      
    
    #UFOlarin hareket komutlari'
    alienX += alienX_change
    
    #ekrani sinirlandirmak icin yapildi
    for i in range(num_of_enemies):
        
        #Game Over
        if score  > 90:
                for j in range(num_of_enemies):
                    alienY[j] =500
                gameover_text()
                break
        
        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
              alienX_change[i] = 8
              alienY[i] += alienY_change[i]
        elif alienX[i] >= 1250:
               alienX_change[i] = -8
               alienY[i] += alienY_change[i]
        #Mermi Etkilesimi
        coll = Collision(alienX[i], alienY[i], rocketX, rocketY)
        if coll:
             explosion_sound = mixer.Sound('explosion.mp3')
             explosion_sound.play()
             rocketY=650
             rocket_state= "Ready!"
             score += 10
             alienX[i]= random.randint(0, 1270)
             alienY[i]=random.randint(50, 150) 
        alien(alienX[i], alienY[i], i)     
           
    #Roket hareket komutlari
    if rocketY <= 0:
         rocketY= 600
         rocket_state= "Ready!"
         
    if rocket_state == "fire":
         fire_rocket(rocketX,  rocketY)
         rocketY -= rocketY_change 
     
    #oyuncunun cagirildigi fonksiyonlar            
    player(playerX, playerY)
    #Skoru ekrana yazdir
    scoreShow(textX, textY)
    #ekrani guncelle
    pygame.display.update()