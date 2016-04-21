import pygame.locals
import time
import PygameHelpers.Button
class PygameHandler():
    def __init__(self, fps):
        pygame.display.init()
        info = pygame.display.Info()
        self.sw = info.current_w
        self.sh = info.current_h
        self.screen = pygame.display.set_mode((self.sw, self.sh), pygame.locals.FULLSCREEN)
        if self.sh * 1.5 <= self.sw:
            self.gw = round(self.sw * (self.sh/800))
            self.gh = self.sh
        else:
            self.gw = self.sw 
            self.gh = round(self.sh * (self.sw/1200))
        self.xoff = (self.sw - self.gw)/2
        self.yoff = (self.sh - self.gh)/2
        self.fps = fps
        self.buttons = []
        self.timers = {}
        self.running = False
        self.buttonPressed = False
        self.timercounter = 0
        self.frames = 0
        self.curTime = time.time()
        self.mouseAction = None
        self.keyLog = []
    def loop(self):
        self.buttonPressed = False
        for event in pygame.event.get():
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.checkPressed(x, y):
                        self.buttonPressed = True
                        break
            elif event.type == pygame.KEYDOWN and event.key not in self.keyLog:
                self.keyLog.append(event.key)
            elif event.type == pygame.locals.QUIT:
                import sys
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0] and self.mouseAction and not self.buttonPressed:
                x, y = pygame.mouse.get_pos()
                self.mouseAction((x,y))
        for timer in dict(self.timers):
            endtime, command = self.timers[timer]
            if self.curTime > endtime:
                command()
                del(self.timers[timer])
        self.frames += 1
    def makeButton(self, coords, width = 10, height = 10, command = None, text = "", clicks = 1, offmain = (0, 0, 0), offedge = (255, 255, 255), onmain = (255, 255, 255), onedge = (0, 0, 0), xRelMiddle = 0.5, yRelMiddle = 0.5):
        colours = offmain, offedge, onmain, onedge
        relMiddle = xRelMiddle, yRelMiddle
        x, y = coords
        x += self.xoff
        y += self.yoff
        button = PygameHelpers.Button.newButton((round(x), round(y)), round(width), round(height), command, text, clicks, colours, relMiddle)
        button.addTimer = self.addTimer
        self.buttons.append(button)
        return button
    def clear(self):
        self.buttons.clear()
    def addTimer(self, command, amount):
        end = amount + time.time()
        counter = self.timercounter
        self.timercounter += 1
        self.timers["after"+ str(counter)] = (end, command)
        return "after" + str(counter)
    def cancelTimer(self, ID):
        if ID in self.timers:
            del(self.timers[ID])
    def stop(self):
        self.running = False
    def setStandardMouseAction(self, command):
        self.mouseAction = command    
def newHandler(fps):
    ph = PygameHandler(fps)
    return ph
