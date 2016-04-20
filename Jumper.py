import math

class Jumper():
    _registry = []
    _fps = None

    def __init__(self, fps):
        self._registry.append(self)
        self._fps = fps
        self.delta = 1/fps
        self.x = 0
        self.y = 0
        self.xspeed = 0
        self.yspeed = 0
        self.maxspeed = 20
        self.maxy = 0
        self.moved = False

    def collisionCheck(self):
        pass

    def update(self):
        self.yspeed += 9.8*self.delta
        if not self.moved and self.xspeed:
            xspeedprev = self.xspeed
            self.xspeed += math.copysign(6*self.delta, -1*self.xspeed)
            if (xspeedprev > 0) ^ (self.xspeed > 0):
                self.xspeed = 0
        # position movement
        self.x += self.xspeed * self.delta
        self.y += self.yspeed * self.delta
        # Temporary floor collision. In future, move floor collision into checkCollision()
        if self.y >= self.maxy:
            self.y = self.maxy
            self.yspeed = 0
        self.moved = False

    def move(self, ximpulse, yimpulse):
        self.moved = True
        self.xspeed += ximpulse * self.delta
        self.yspeed += yimpulse * self.delta
        if math.fabs(self.xspeed) > self.maxspeed:
            self.xspeed = math.copysign(self.maxspeed, self.xspeed)
        if self.yspeed > self.maxspeed:
            self.yspeed = self.maxspeed

    def render(self, screen): #Call this in the Main update loop. It should draw the object to the screen
        pass