# Ideas mostly taken from this bloke ==> Paul Vincent Craven

import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)
red = (255, 0, 0)

screen_width = 800
screen_height = 600


class Wall(pygame.sprite.Sprite):
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
        self.image = pygame.Surface([15, 15])
        self.image.fill(white)

        # sets it to the top left of the numbers
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # set a speed constant
        self.speed_x = 0
        self.speed_y = 0

    def accelerate(self, a_x, a_y):
        self.speed_x += a_x
        self.speed_y += a_y

    def move(self, walls, enemies):
        # Move left/right
        self.rect.x += self.speed_x

        # check if it hit anything
        # takes the object itself, what it hits, and checks whether it should destroy it (False)
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # move the sprite to a place that is totally fine to be at
            if self.speed_x > 0:  # ie going right
                self.rect.right = block.rect.left
            else:  # if the block is going left
                self.rect.left = block.rect.right

        # and now to move it up and down
        self.rect.y += self.speed_y

        # same as above, does them separately just in case moving it made it hit something else
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        if pygame.sprite.spritecollideany(self, enemies, False):
            for n in range(30):
                print("U dead gurl")
            return True




class Enemy(pygame.sprite.Sprite):
    def __init__(self, xinit, yinit, xfin, yfin):
        super().__init__()

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

    def move(self):
        if self.rect.y <= self.yinit and self.rect.x < self.xfin:
            self.rect.x += 6
        elif self.rect.x >= self.xfin and self.rect.y < self.yfin:
            self.rect.y += 6
        elif self.rect.y >= self.yfin and self.rect.x > self.xinit:
            self.rect.x -= 6
        elif self.rect.x <= self.xinit and self.rect.y > self.yinit:
            self.rect.y -= 6


class Room(object):
    # base class for rooms

    # rooms have list of stuff
    wall_list = None
    enemies = None
    coins = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()


class Room1(Room):
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, white],
                 [0, 350, 20, 250, white],
                 [780, 0, 20, 250, white],
                 [780, 350, 20, 250, white],
                 [20, 0, 760, 20, white],
                 [20, 580, 760, 20, white],
                 [390, 50, 20, 500, blue]
                ]

        enemy = Enemy(30, 30, 370, 560)
        self.enemies.add(enemy)

        for w in walls:
            wall = Wall(w[0], w[1], w[2], w[3], w[4])
            self.wall_list.add(wall)


class Room2(Room):
    """This creates all the walls in room 2"""
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, white],
                 [0, 350, 20, 250, white],
                 [780, 0, 20, 250, white],
                 [780, 350, 20, 250, white],
                 [20, 0, 760, 20, white],
                 [20, 580, 760, 20, white],
                 [190, 50, 20, 500, blue],
                 [590, 50, 20, 500, blue]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room3(Room):
    """This creates all the walls in room 3"""
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, white],
                 [0, 350, 20, 250, white],
                 [780, 0, 20, 250, white],
                 [780, 350, 20, 250, white],
                 [20, 0, 760, 20, white],
                 [20, 580, 760, 20,  white]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, blue)
                self.wall_list.add(wall)

        for x in range(150, 700, 100):
            wall = Wall(x, 200, 20, 200, blue)
            self.wall_list.add(wall)

# Now that's all done, lets actually test this stuff.
def main():
    pygame.init()

    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("Let's seeeeeeeee......")

    moving_sprites = pygame.sprite.Group()
    """not really a """
    jumper = Jumper(0, 293)
    moving_sprites.add(jumper)

    rooms = []

    room = Room1()
    rooms.append(room)

    room = Room2()
    rooms.append(room)

    room = Room3()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()

    done = False

    speed = 3
    while not done:
        # key checks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jumper.accelerate(-speed, 0)
                elif event.key == pygame.K_RIGHT:
                    jumper.accelerate(speed, 0)
                elif event.key == pygame.K_UP:
                    jumper.accelerate(0, -speed)
                elif event.key == pygame.K_DOWN:
                    jumper.accelerate(0, speed)

            # we can mess with this with ice and other surfaces
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    jumper.accelerate(speed, 0)
                elif event.key == pygame.K_RIGHT:
                    jumper.accelerate(-speed, 0)
                elif event.key == pygame.K_UP:
                    jumper.accelerate(0, speed)
                elif event.key == pygame.K_DOWN:
                    jumper.accelerate(0, -speed)

        # room moving
        done = jumper.move(current_room.wall_list, current_room.enemies)

        for enemy in current_room.enemies:
            enemy.move()

        if jumper.rect.x < -15:
            if current_room_no == 0:
                for enemy in current_room.enemies:
                    moving_sprites.remove(enemy)
                current_room_no = 2
                current_room = rooms[current_room_no]
                for enemy in current_room.enemies:
                    moving_sprites.add(enemy)
                jumper.rect.x = 790
            elif current_room_no == 2:
                for enemy in current_room.enemies:
                    moving_sprites.remove(enemy)
                current_room_no = 1
                current_room = rooms[current_room_no]
                jumper.rect.x = 790
            else:
                for enemy in current_room.enemies:
                    moving_sprites.remove(enemy)
                current_room_no = 0
                current_room = rooms[current_room_no]
                jumper.rect.x = 790

        if jumper.rect.x > 801:
            if current_room_no == 0:
                for enemy in current_room.enemies:
                    moving_sprites.remove(enemy)
                current_room_no = 1
                current_room = rooms[current_room_no]
                jumper.rect.x = 0
            elif current_room_no == 1:
                for enemy in current_room.enemies:
                    moving_sprites.remove(enemy)
                current_room_no = 2
                current_room = rooms[current_room_no]
                jumper.rect.x = 0
            else:
                for enemy in current_room.enemies:
                    moving_sprites.remove(enemy)
                current_room_no = 0
                current_room = rooms[current_room_no]
                jumper.rect.x = 0

        # now draw! ^-^
        screen.fill(black)

        moving_sprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

main()

pygame.quit()
