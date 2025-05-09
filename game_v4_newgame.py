import pygame, random
#import all the libraries of code that we need for our game
from pygame.locals import *

#initiaze the game engine
pygame.init()

#create a 2d vector object so we can do game physics like motion and gravity
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400

#constants to use for my game physics later
ACC = 0.5 #acceleration due to gravity
FRIC = -0.12 #friction

#constants for frame rate
FPS = 60

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("images/test.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf,(70,90))
        self.rect = self.surf.get_rect()

       

        self.pos = vec((10,130))
        self.vel = vec(0,0)
        self.acc = vec(0,0.5)

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -0.5
        if pressed_keys[K_RIGHT]:
            self.acc.x = 0.5

        #equations of motion a.k.a physics math
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 *self.acc

        #aplly the new position to the rectangle object that represents the player 
        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits:
            self.vel.y = 0
            self.pos.y = hits[0].rect.top + 1

    def jump(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits:
            self.vel.y = -15

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((153,76,0))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH-10), random.randint(0, HEIGHT-30)))
        self.pos = vec((20, 380))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

#this is the ground
PT1 = Platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((0,153,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
#create a player
P1 = Player()
print(P1.rect.center)


#create a group object to hold all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PT1)

platforms = pygame.sprite.Group()
platforms.add(PT1)


#make a clock to use the frames per second later
clock1 = pygame.time.Clock()

#crerate a window for the game
pygame.display.set_caption("Jungle Rush")


#initalizing level genration
#generates the platoform that appear at the start of the game

for x in range(random.randint(3,6)):
    plat = Platform()
    platforms.add(plat)
    all_sprites.add(plat)

#functions for the whole game 
def plat_gen():
    while len(platforms) <7:
        width = random.randrange(50,100)
        p = Platform()
        platforms.add(p)
        all_sprites.add(p)

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load('Sounds/soundtrack.mp3')
pygame.mixer.music.play(-1) #-1 means loops for ever, 0 means play just once)


background = pygame.image.load("images/Forest-Transparent.jpg")



#-----------------------GAME LOOP-----------------------------------------
#variable that stores a boolean values (True or False)
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    P1.jump()

    if P1.rect.bottom <= HEIGHT / 3: #checks the position of the player
        P1.pos.y += abs(P1.vel.y) #updates the position of the plater as the screen "moves"
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y) #updates the position of the platforms on the screen
            if plat.rect.top >= HEIGHT: #if the platform gets to the bottom of the screen...
                plat.kill() #distroy the platform in the memory to free up memory space
   
   
   
    P1.move()
    P1.update()
    plat_gen()


    #clears the screen every loop by filling it with a color
    displaysurface.fill((0,0,0))

    displaysurface.blit(background, (0, 0))

    #draw all the sprties in a group
    for item in all_sprites:
        displaysurface.blit(item.surf, item.rect)
    
    print(P1.rect)
  

    #update the display every game loop
    pygame.display.update()

    #make a clock to control the frame rate 
    clock1.tick(FPS)
    

    

#after you exit the game loop
#quite the game engine
pygame.quit()


