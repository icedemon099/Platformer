class Jumper():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.yVel = 0
        self.xVel = 0
    def collisionCheck(self):
        pass
    def update(self):
        self.yVel += 9.8 #Gravity
        self.x += self.xVel
        self.y += self.yVel
    def move(self, xAcc, yAcc):
        self.xVel += xAcc
        self.yVel += yAcc