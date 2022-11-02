import pygame,math,sys, colorsys
import paddel
from pygame.locals import *
from bg import Background
import random
# Initialize pygame package
pygame.init()

# Pygame Screen
screen_width=640
screen_height=480
screen=pygame.display.set_mode((screen_width,screen_height))

#game variables
GRAVITY = 1
MAX_PLATFORMS = 10
WHITE = (0,0,0)

# Display and Buttons
pygame.display.set_caption('Get a Job')
icon=pygame.image.load('bag.png')
pygame.display.set_icon(icon)

#Player
playerIMG=pygame.image.load('graduate (2).png')
playerX=370
playerY=350

#Ledge
ledgeIMG=pygame.image.load('remove.png')
ledgeX=370
ledgeY=350
Xchange=0.3
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)


class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(playerIMG, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        # reset variables
        dx = 0
        dy = 0

        # process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        # check collision with platforms
        for platform in platform_group:
            # collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        # check collision with ground
        if self.rect.bottom + dy > screen_height:
            dy = 0
            self.vel_y = -20

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ledgeIMG, (width, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def move(self):
        #reset movement direction
        key = pygame.key.get_pressed()
        if self.direction == -1 and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if self.direction == -1 and self.rect.left < 5:
            self.rect.x += self.speed
            self.direction = 1
        if self.direction == 1 and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1
        if self.direction == 1 and self.rect.right == 595:
            self.rect.x -= self.speed
            self.direction = -1
        print(self.rect.left)


player = Player(screen_width // 2, screen_height - 150)



# create sprite groups
platform_group = pygame.sprite.Group()

# create temporary platforms
for p in range(MAX_PLATFORMS):
    p_w = random.randint(40, 60)
    p_x = random.randint(0, screen_width - p_w)
    p_y = p * random.randint(80, 120)
    platform = Paddle(p_x, p_y, p_w)
    platform_group.add(platform)



# Game Loop
running=True
while running:
    screen.fill((0,0,0))
    playerY+=1.5
    player.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if playerX <0:
        playerX=0
    bg = [Background(), Background(), Background()]
    for o in bg:
        o.setSprite((playerY % 100) / 100)
        screen.blit(o.sprite, (0, o.position))

    player.draw()
    platform_group.draw(screen)
    pygame.display.update()
