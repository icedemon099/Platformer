#Class Map
#The "Map" is the stage
#It has a size limit and
#This is where you should define
#the locations of the different
#and walls
class Map():
    def __init__(self, minX, maxX, minY, maxY):
        self.minX, self.maxX, self.minY, self.maxY = minX, maxX, minY, maxY #These dimesions can change
