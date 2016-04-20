
# Import libraries
import pygame.locals
import time
from math import *
from sys import exit
#
# Import code
import Jumper

# Setup game
pygame.init()
screen = pygame.display.set_mode((200,200))

fps = 30

player = Jumper.Jumper(fps, 50, 50)
lastprint = time.time()

# Main loop
while True:
    timeprev = time.time()

    # Movement input
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        player.move(-8, 0)
    if pressed[pygame.K_RIGHT]:
        player.move(8, 0)
    if pressed[pygame.K_UP]:
        player.move(0, -12)
    if pressed[pygame.K_DOWN]:
        player.move(0, 3)

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            exit()

    player.update()
    screen.fill((255,255,255))
    player.render(screen)
    pygame.display.flip()
    # Delta timing
    timedelta = time.time()-timeprev
    if time.time() > lastprint + 1:
        print(player.x, player.y, player.xspeed, player.yspeed)
        lastprint = time.time()
    if timedelta < player.delta:
        time.sleep(player.delta-timedelta)
    else:
        print("Overloaded")