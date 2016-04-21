import pygame
class Button():
    def __init__(self, coords, width, height, command, text, clicks, colours, relMiddle):
        #X and Y refer to where to draw the button
        #Command is the function invoked when the buttons is clicked
        #clicks is the number of times the buttton needs to be
        #clicked in a row to invoke the command
        #Colours refer to the color of the buttons edge are button when clicked 
        #and not clicked
        #relMiddle tells the program how to anchor the button based of the coordinates
        #Since pygame always uses the coordinate given for the top corner
        
        self.x, self.y = coords
        self.width = width
        self.height = height
        self.offmain, self.offedge, self.onmain, self.onedge = colours
        self.width = width
        self.height = height
        self.command = command
        self.clicks = clicks
        self.timesclicked = 0
        self.addTimer = None
        
        #immediately after the button is made this is changed
        #to a link to a pygame_handler function of the same name
        
        self.drawme = False

        #If false, not drawn and is unable to be clicked
        
        self.updateText(text)
        self.changeAnchor(relMiddle)
    def checkPressed(self, x, y):
        #If clicked, will invoke its command if its been clicked enough times
        #recently, and returns True to let the caller know to
        #stop checking for button clicks
        
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height) and self.drawme:
            self.timesclicked += 1
            if self.timesclicked == self.clicks:
                self.command() 
            self.addTimer(self.reset, 0.1)
            return True
        return False
    def invoke(self):
        if self.drawme:
            self.timesclicked += 1
            if self.timesclicked == self.clicks:
                self.command() 
            self.addTimer(self.reset, 0.1)
    def reset(self):
        #Called after 0.1 seconds after a button is clicked
        #resets the number of times the button has been clicked recently
        #Also means a button can't be clicked multiple times in the space of
        #0.1 seconds.
        
        if self.timesclicked >= self.clicks:
            self.timesclicked = 0
        elif self.timesclicked > 0:
            self.timesclicked -=1
    def draw(self):
        if self.drawme:
            screen = pygame.display.get_surface()
            if self.timesclicked >= self.clicks:
                pygame.draw.rect(screen, (self.onmain), (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, (self.onedge), (self.x - self.width/40, self.y - self.width/40, self.width + (self.width/40)*2 - 1, self.height + (self.width/40)*2 -1), round(self.width/40)+1)
            else:
                pygame.draw.rect(screen, (self.offmain), (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, (self.offedge), (self.x - self.width/40, self.y - self.width/40, self.width + (self.width/40)*2 - 1, self.height + (self.width/40)*2 -1), round(self.width/40)+1)

            #Changes colour if selected. The rim will be a different colour
                
            screen.blit(self.text, (self.x, self.y))
    def updateText(self, text):
        #Finds the maximum size the text can be to fit, and creates the text
        #to be rendered when draw() is called
        
        size = 0
        while True:
            self.font = pygame.font.Font(None, size + 1)
            fwidth, fheight = self.font.size(text)
            if fheight >= self.height  or fwidth >= self.width:
                break
            size += 1
        self.font = pygame.font.Font(None, size)
        self.text = self.font.render(text, 1, (255,255,0))
    def changeAnchor(self, relMiddle):
        #adjusts the x and y so that the original coordinates can be used
        #for a different point on the button, rather than the top
        #left corner
        
        xRelMiddle, yRelMiddle = relMiddle
        self.x -= round(self.width*xRelMiddle)
        self.y -= round(self.height*yRelMiddle)
def newButton(coords, width, height, command, text, clicks, colours, relCentre):
    button = Button(coords, width, height, command, text, clicks, colours, relCentre)
    return button
