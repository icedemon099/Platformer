# Ideas mostly taken from this bloke ==> Paul Vincent Craven
# And I'm sorry I made this, this is mostly for me to understand how pygame works...
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)
red = (255, 0, 0)

screen_width = 800
screen_height = 600


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour):
        # uses parent sprite module section - need to learn more bout this
        # walls can only be straight rectangles at this point in time, unfortunately.
        super().__init__()

        # makes the wall blue and sets the size
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)

        #  make top left corner the location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Jumper(pygame.sprite.Sprite):  # (which doesn't jump yet) >v<

    def __init__(self, x, y):
        super().__init__()

        # creates a surface just like before and makes it white
        self.image = pygame.Surface([20, 50])
        self.image.fill(white)

        # sets it to the top left of the numbers
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # set a speed constant
        self.speed_x = 0
        self.speed_y = 0

        self.level = None

    def update(self):
        self.calc_grav()

        # Move left/right
        self.rect.x += self.speed_x

        # check if it hit anything
        # takes the object itself, what it hits, and checks whether it should destroy it (False)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # move the sprite to a place that is totally fine to be at
            if self.speed_x > 0:  # ie going right
                self.rect.right = block.rect.left
            elif self.speed_x < 0:  # if the block is going left
                self.rect.left = block.rect.right

        # and now to move it up and down
        self.rect.y += self.speed_y

        # same as above, does them separately just in case moving it made it hit something else
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
            elif self.speed_y < 0:
                self.rect.top = block.rect.bottom
            # stop vertical movement
            self.speed_y = 0


    def calc_grav(self):
        # find effect of gravity
        if self.speed_y == 0:
            self.speed_y = 1  # cos if the block is moving, the player's gotta move with it too
        else:
            self.speed_y += .35

    def jump(self):
        # when jump button is hit

        # move down a bit to check that there is a floor
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0:
            self.speed_y = -10

    def checkdeath(self):
        # hit = death

        if pygame.sprite.spritecollideany(self, self.level.enemies, False):
            for n in range(30):
                print("U dead gurl")
            return True


# class for enemy, you can make as many classes for this stuff, its fun!
class Enemy(pygame.sprite.Sprite):
    def __init__(self, xinit, yinit, xfin, yfin):
        super().__init__()

        # same stuff as jumper
        self.image = pygame.Surface([10, 10])
        self.image.fill(red)

        # sets it to the top left of the numbers
        self.rect = self.image.get_rect()
        self.xinit = xinit
        self.yinit = yinit
        self.rect.x = xinit
        self.rect.y = yinit
        self.xfin = xfin
        self.yfin = yfin

    def update(self):
        # moves the enemy in a rectangle based on xinit, yinit, xfin, and yfin.
        if self.rect.y <= self.yinit and self.rect.x < self.xfin:
            self.rect.x += 6
        elif self.rect.x >= self.xfin and self.rect.y < self.yfin:
            self.rect.y += 6
        elif self.rect.y >= self.yfin and self.rect.x > self.xinit:
            self.rect.x -= 6
        elif self.rect.x <= self.xinit and self.rect.y > self.yinit:
            self.rect.y -= 6


class Level(object):
    # base class for rooms

    # initialises stuff lists
    def __init__(self, jumper):
        self.platform_list = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.jumper = jumper
        self.coins = pygame.sprite.Group()

        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemies.update()

    def draw(self, screen):
        # draws the stuff
        screen.fill(blue)

        self.platform_list.draw(screen)
        self.enemies.draw(screen)


class Level_01(Level):
    def __init__(self, jumper):
        Level.__init__(self, jumper)

        # wall data
        level = [[0, 0, 20, 250, white],
                 [0, 350, 20, 250, white],
                 [780, 0, 20, 250, white],
                 [780, 350, 20, 250, white],
                 [20, 0, 760, 20, white],
                 [20, 580, 760, 20, white],
                 [500, 500, 210, 70, black],
                 [200, 400, 210, 70, black],
                 [600, 300, 210, 70, black]
                ]

        # makes enemy
        enemy = Enemy(30, 30, 370, 560)
        enemy.jumper = self.jumper
        self.enemies.add(enemy)

        # makes walls
        for p in level:
            platform = Platform(p[0], p[1], p[2], p[3], p[4])
            platform.jumper = self.jumper
            self.platform_list.add(platform)


# Now that's all done, lets actually test this stuff.
def main():
    pygame.init()

    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("Let's see......")

    # creates jumper
    moving_sprites = pygame.sprite.Group()
    """not really a """
    jumper = Jumper(0, 293)
    moving_sprites.add(jumper)

    # adds rooms to list and initialises them
    levels = []

    level = Level_01(jumper)
    levels.append(level)

    current_level_no = 0
    current_level = levels[current_level_no]

    jumper.level = current_level

    for enemy in current_level.enemies:
        moving_sprites.add(enemy)

    # sorry bout the clock, I'll add in some more info bout it later
    clock = pygame.time.Clock()

    done = False

    speed = 6
    # main loop for movement and checking user input
    while not done:
        # key checks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jumper.speed_x = -speed
                elif event.key == pygame.K_RIGHT:
                    jumper.speed_x = speed
                elif event.key == pygame.K_UP:
                    jumper.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and jumper.speed_x < 0:
                    jumper.speed_x = 0
                if event.key == pygame.K_RIGHT and jumper.speed_x > 0:
                    jumper.speed_x = 0

        # moving the sprites
        moving_sprites.update()
        current_level.update()

        # check death
        if jumper.checkdeath():
            done = True

        # can't go beyond as of yet
        if jumper.rect.right > screen_width:
            jumper.rect.right = screen_width
        if jumper.rect.left < 0:
            jumper.rect.left = 0

        # now draw! ^-^
        current_level.draw(screen)  # redraws walls
        moving_sprites.draw(screen)  # redraws moving sprites

        pygame.display.flip()
        clock.tick(60)

main()

pygame.quit()
