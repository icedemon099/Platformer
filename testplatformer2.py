# Ideas mostly taken from this bloke ==> Paul Vincent Craven
# And I'm sorry I made this, this is mostly for me to understand how pygame works...
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)
red = (255, 0, 0)
green = (50, 255, 50)

screen_width = 800
screen_height = 600


class Platform(pygame.sprite.Sprite):
    colour = black
    width = 10
    height = 10

    def __init__(self):
        # uses parent sprite module section - need to learn more bout this
        # walls can only be straight rectangles at this point in time, unfortunately.
        super().__init__()

    def make(self, x, y):
        # makes the wall blue and sets the size
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)

        #  make top left corner the location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x



class MovingPlatform(Platform):
    speed_x = 0
    speed_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
    cur_pos = 0
    player = None

    level = None
    colour = green

    def __init__(self):
        super().__init__()

    def update(self):
        # mooooove da jumper - same method as jumper

        # Move left/right
        self.rect.x += self.speed_x

        # Did we hit a jumper?
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # Shove the jumper away - the platform's more important.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.speed_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.speed_y

        # same for up and down
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # Push the jumper
            if self.speed_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Do we need to change direction after hitting boundary limit?
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.speed_y *= -1

        # need to consider world shift
        self.cur_pos += self.speed_x
        if self.cur_pos < self.boundary_left or self.cur_pos > self.boundary_right:
            self.speed_x *= -1


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
            if isinstance(block, MovingPlatform):
                self.rect.x += block.speed_x
                print("iM ON MBLOCK")
                print(block.speed_x)
                print(self.rect.x)
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

        if self.rect.y >= screen_height - self.rect.height and self.speed_y >= 0:
            self.speed_y = 0
            self.rect.y = screen_height - self.rect.height

    def jump(self):
        # when jump button is hit

        # move down a bit to check that there is a floor
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= screen_height:
            self.speed_y = -10

    def checkdeath(self):
        # hit = death

        if pygame.sprite.spritecollideany(self, self.level.enemies, False):
            for n in range(30):
                print("U dead gurl")
            return True


# class for enemy, you can make as many classes for this stuff, its fun!
class Enemy(pygame.sprite.Sprite):
    def __init__(self, xinit, yinit, xdis, ydis):
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
        self.dis = (xdis, ydis)
        self.currentdis = [0, 0]

    def update(self):

        # moves the bloke in a rectangle
        if self.currentdis[0] <= self.dis[0] and self.currentdis[1] <= 0:
            self.rect.x += 6
            self.currentdis[0] += 6
        elif self.currentdis[0] >= self.dis[0] and self.currentdis[1] <= self.dis[1]:
            self.rect.y += 6
            self.currentdis[1] += 6
        elif self.currentdis[0] >= 0 and self.currentdis[1] >= self.dis[1]:
            self.rect.x -= 6
            self.currentdis[0] -= 6
        elif self.currentdis[0] <= 0 and self.currentdis[1] >= 0:
            self.rect.y -= 6
            self.currentdis[1] -= 6


class Level(object):
    # base class for rooms

    # initialises stuff lists
    def __init__(self, jumper):
        self.platform_list = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.jumper = jumper
        self.coins = pygame.sprite.Group()

        self.world_shift = 0

        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemies.update()

    def draw(self, screen):
        # draws the stuff
        screen.fill(blue)

        self.platform_list.draw(screen)
        self.enemies.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemies:
            enemy.rect.x += shift_x


class Level_01(Level):
    def __init__(self, jumper):
        Level.__init__(self, jumper)

        # wall data
        level = [[500, 520, 210, 70, black],
                 [200, 400, 210, 70, black],
                 [580, 350, 210, 70, black]
                ]

        self.level_limit = -1000
        # makes enemy
        enemy = Enemy(30, 30, 370, 560)
        enemy.jumper = self.jumper
        self.enemies.add(enemy)

        mp = MovingPlatform()
        self.platform_list.add(mp)
        mp.width = 120
        mp.height = 20
        mp.boundary_left = 0
        mp.boundary_right = 200
        mp.speed_x = 3
        mp.player = self.jumper
        mp.level = self
        mp.make(300, 250)


        # makes walls
        for p in level:
            platform = Platform()
            platform.width = p[2]
            platform.height = p[3]
            platform.colour = p[4]
            platform.make(p[0], p[1])
            platform.jumper = self.jumper
            self.platform_list.add(platform)


class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [[450, 570, 210, 30, black],
                 [850, 420, 210, 30, black],
                 [1000, 520, 210, 30, black],
                 [1120, 280, 210, 30, black],
                 ]

        # Go through the array above and add platforms
        for p in level:
            platform = Platform()
            platform.width = p[2]
            platform.height = p[3]
            platform.colour = p[4]
            platform.make(p[0], p[1])
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

    level = Level_02(jumper)
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

        # If the player gets near the right side, shift the world left (-x)
        if jumper.rect.right >= 500:
            diff = jumper.rect.right - 500
            jumper.rect.right = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if jumper.rect.left <= 120:
            diff = 120 - jumper.rect.left
            jumper.rect.left = 120
            current_level.shift_world(diff)

        current_pos = jumper.rect.x + current_level.world_shift
        if current_pos < current_level.level_limit:
            jumper.rect.x = 120
            if current_level_no < len(levels) - 1:
                current_level_no += 1
                current_level = levels[current_level_no]
                jumper.level = current_level

        # now draw! ^-^
        current_level.draw(screen)  # redraws walls
        moving_sprites.draw(screen) # redraws moving sprites

        pygame.display.flip()
        clock.tick(60)

main()

pygame.quit()
