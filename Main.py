
# Import libraries
import pygame.locals
import time
from math import *
from sys import exit

# Import code
import Jumper

# Setup game
pygame.init()
info = pygame.display.Info()
sw = info.current_w
sh = info.current_h
screen = pygame.display.set_mode((sw, sh))

fps = 60
pixelFactor = 20
tickTime = 1/fps  # I dont mind if you rename this, but i dont find delta to be a clear name
sprites = pygame.sprite.Group()
player = Jumper.Jumper(fps, pixelFactor/2, pixelFactor)
lastprint = time.time()

xAccelaration = 12
# Main loop
while True:
    timeprev = time.time()

    # Movement input
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        player.move(-xAccelaration, 0)
    if pressed[pygame.K_RIGHT]:
        player.move(xAccelaration, 0)
    if pressed[pygame.K_UP]:
        # Positive direction is UP. Do not change
        player.move(0, fps*12)
    if pressed[pygame.K_DOWN]:
        player.move(0, 5)

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
    if timedelta < tickTime:
        time.sleep(player.tickTime - timedelta)
    else:
        print("Overloaded")