from math import *
import pygame.locals
import time
import Jumper
pygame.init()
pygame.display.set_mode((200,200))
fps = 30
Jumper = Jumper.Jumper(fps)
lastPrint = time.time()
while True:
    lastTime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Jumper.move((-8)/fps,0)
            elif event.key == pygame.K_RIGHT:
                Jumper.move((8)/fps,0)
            elif event.key == pygame.K_UP:
                Jumper.move(0,(12)/fps)
            elif event.key == pygame.K_DOWN:
                Jumper.move(0,(-3)/fps)
        elif event.type == pygame.locals.QUIT:
            import sys
            pygame.quit()
            sys.exit()
    Jumper.update()
    if time.time() > lastPrint + 1:
        print(Jumper.x, Jumper.y)
        lastPrint = time.time()
    lostTime = time.time()-lastTime
    if lostTime < (1/fps):
        time.sleep((1/fps)-lostTime)
    else:
        print("Overloaded")