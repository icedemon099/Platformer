
# Import libraries
import pygame.locals
import time
from math import *

# Import code
import Jumper

# Setup game
pygame.init()
pygame.display.set_mode((200,200))

fps = 30
a = 1
b = 2

Jumper = Jumper.Jumper(fps)
lastPrint = time.time()

# Main loop
while True:
    lastTime = time.time()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        Jumper.move((-8)/fps,0)
    if pressed[pygame.K_RIGHT]:
        Jumper.move((8)/fps,0)
    if pressed[pygame.K_UP]:
        Jumper.move(0,(12)/fps)
    if pressed[pygame.K_DOWN]:
        Jumper.move(0,(-3)/fps)
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            import sys
            pygame.quit()
            sys.exit()
    Jumper.update()
    if time.time() > lastPrint + 1:
        print(Jumper.x, Jumper.y, Jumper.yVel)
        lastPrint = time.time()
    lostTime = time.time()-lastTime
    if lostTime < (1/fps):
        time.sleep((1/fps)-lostTime)
    else:
        print("Overloaded")