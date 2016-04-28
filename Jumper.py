import math
import pygame
class Jumper(pygame.sprite.Sprite):
    _registry = []
    _fps = None
    _sw = None
    _sh = None
    def __init__(self, fps, width, pixelFactor):
        #Coords are the TOP LEFT CORNER. This is for pygame.mask
        super().__init__()
        self._registry.append(self)
        self._fps = fps
        self._sw = pygame.display.Info().current_w
        self._sh = pygame.display.Info().current_h
        self.tickTime = 1 / fps
        self.x = 0
        self.y = width
        self.xspeed = 0
        self.yspeed = 0
        self.maxspeed = 20
        self.miny = 0
        self.moved = False
        self.width = width
        self.pixelFactor = pixelFactor #Pixels per in-game meter. Feel free to adjust
        self.colAcc = 1 #Short for Collison accuracy. The full name is to long to fit on other lines. Feel free to change
        #I'm using mask to all for no-rectangler collision.
        self.image = pygame.transform.scale(pygame.image.load("dog.gif").convert_alpha(), (round(width*pixelFactor),round(width*pixelFactor)))
        self.mask = pygame.mask.from_surface(self.image, 127)#Needs an alpha off greater than 127 to count. Placeholder
        self.rect = self.image.get_rect()

    def collisionCheck(self):
        pass

    def update(self):
        self.yspeed += -9.8*self.tickTime
        if not self.moved and self.xspeed:
            xspeedprev = self.xspeed
            self.xspeed += math.copysign(6 * self.tickTime, -1 * self.xspeed)
            if (xspeedprev > 0) ^ (self.xspeed > 0):
                self.xspeed = 0
        # position movement
        self.x += self.xspeed * self.tickTime
        self.y += self.yspeed * self.tickTime
        # Temporary floor collision. In future, move floor collision into checkCollision()
        if self.y-self.width <= self.miny:
            self.y = self.miny
            self.yspeed = 0
        self.moved = False
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask.set_at((self.rect.x, self.rect.y))
    def move(self, ximpulse, yimpulse):
        self.moved = True
        self.xspeed += ximpulse * self.tickTime
        self.yspeed += yimpulse * self.tickTime
        if math.fabs(self.xspeed) > self.maxspeed:
            self.xspeed = math.copysign(self.maxspeed, self.xspeed)
        if self.yspeed > self.maxspeed:
            self.yspeed = self.maxspeed

    def render(self, screen): #Call this in the Main update loop. It should draw the object to the screen
        pygame.draw.circle(screen, (0, 0, 0), (round((self.x-(self.width/2))*self.pixelFactor), self._sh-round((self.y-(self.width/2))*self.pixelFactor)), self.width)
