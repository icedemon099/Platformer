import math
class Jumper():
    def __init__(self, fps):
        self.x = 0
        self.y = 0
        self.yVel = 0
        self.xVel = 0
        self.fps = fps
        self.maxRunSpeed = 20
        self.minY = 0
        self.moved = False
    def collisionCheck(self):
        pass
    def update(self):
        self.yVel -= 9.8*(1/self.fps) #Gravity
        if not self.moved and self.xVel:
            oldXVel = self.xVel
            self.xVel += math.copysign(6 * (1/self.fps),-1*self.xVel)
            if (oldXVel>0) ^ (self.xVel>0): # ^ is the xor function. This will return true if ONE of those statements is true, but not both
                self.xVel = 0
        self.x += self.xVel * (1/self.fps)
        self.y += self.yVel * (1/self.fps)
        if self.y < self.minY:
            self.y = self.minY
            self.yVel = 0
        self.moved = False
    def move(self, xAcc, yAcc):
        self.moved = True
        self.xVel += xAcc
        self.yVel += yAcc
        if math.fabs(self.xVel) > self.maxRunSpeed:
            self.xVel = math.copysign(self.maxRunSpeed, self.xVel)
        if self.yVel > self.maxRunSpeed:
            self.yVel = self.maxRunSpeed