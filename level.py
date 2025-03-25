import pygame
import time
import math
import json

window_x = 800
window_y = 600


level_1 = [
    "................................",
    ".AAAAAAAA.......................",
    ".A..............................",
    ".A..............................",
    ".AAAAAAAA.......................",
    "................................",
    "................................",
    ".................AAAAAAAAAAAAAAA",
    "..AAAA..........................",
    "................................",
    "....AAAAAAAAA...................",
    "................................",
    "................................",
    ".................AAAAAAAAAAA....",
    "................................",
    "................................",
    "AAAAAAAAAAAAAA..................",
    "................................",
    "..............AAA...............",
    "................................",
    ".........................AAAAAAA",
    "................................",
    "................................",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA....",
]

# platform[0] -> x
# platform[1] -> y
# platform[2] -> width
# platform[3] -> height

def loadLevel(level):
    scale_factor = 48
    platforms = []
    for row_idx, row in enumerate(level):
        for col_idx, cell in enumerate(row):
            if cell != '.':
                # x, y, width, height
                platforms.append((
                    scale_factor * col_idx,
                    scale_factor * row_idx,
                    scale_factor,
                    scale_factor,
                ))
    return platforms

class Player:
    def __init__(self):
        # our player's absolute position
        self.x = 0
        self.y = 600 - 40
        # our player's size
        self.width = 30
        self.height = 40
        # our player's velocity
        self.vel = 5
        # for the jump function
        self.isJump = False
        # this is used to adjust the jump height
        self.default_jumpCount = 35
        self.jumpCount = self.default_jumpCount

# rect is (x[0], y[1], width[2], height[3])

    # function for jump and collision detect
    def jump_update(self, platforms, elapsed):
        if self.isJump:
            # if self.jumpCount >= -40: (this was used to make the jump has the same landing as when it started to jump)
            # if the player's y + it's height is not below than the bottom of the screen, enable the jump, otherwise, set player's y level to the bottom of the screen plus it's height and disable the jump_update
            if not self.y + self.height > window_y:
                for platform in platforms:
                    # collision detect for platform_0 (bottom)
                    # if player's position is between the bottom of the platform_0
                    if (self.y < platform[1] + platform[3]) and \
                    (self.y + self.height >= platform[1] + platform[3]) and \
                    (self.x <= platform[0] + platform[2]) and \
                    (self.x + self.width >= platform['x']):
                        # set player to free fall and it's y level to the bottom of the platform_0
                        self.jumpCount = 0
                        self.y = platform[1] + platform[3]

                    # collision detect for platform_1 (top)
                    # if player's position is between the top of the platform_1
                    if (self.y <= platform[1]) and \
                    (self.y + self.height >= platform[1]) and \
                    (self.x <= platform[2]):
                        # set player's y level to the top of the platform_1 and disable the jump update
                        self.y = platform[1] - self.height
                        self.jumpCount = self.default_jumpCount
                        self.isJump = False

                # jump_update function
                # this 0.00.. is used to control the jump speed, and it will influence the jump height too
                self.y -= (self.jumpCount * abs(self.jumpCount)) * elapsed
                self.jumpCount -= 1


            else: 
                self.y = window_y - self.height
                self.jumpCount = self.default_jumpCount
                self.isJump = False
            # if self.jumpCount >= -10:
            #     self.neg = 1
            #     if self.jumpCount < 0:
            #         self.neg = -1
            #     self.y -= (self.jumpCount ** 2) * 0.5 * self.neg
            #     self.jumpCount -= 1
            # else:
            #     self.jumpCount = 10
            #     self.isJump = False
                
    # our position is changed based on our velocity
    # Our current velocity is also changed by gravity
    def update_position(self, screen, platforms, elapsed):
        (self.world_x, self.world_y) = screen.get_size()

        # stores keys pressed 
        keys = pygame.key.get_pressed() 
        
        # if A key is pressed 
        if keys[pygame.K_a] and self.x > 0: 
            
            # free fall at the left edge of the platform_0
            # if it's right edge leave the tip of the platform_0
            if (self.x + self.width <= platform_0['x']) and \
            (self.x + self.width >= platform_0['x'] - 1) and \
            (self.y + self.height == platform_0['y']):
                # let the player free fall
                self.jumpCount = 0
                self.isJump = True
            # decrement in x co-ordinate 
            self.x -= self.vel
            
        # if D key is pressed 
        if keys[pygame.K_d] and self.x < self.world_x - self.width: 

            # free fall at the right edge of the platform_1
            # if player's left edge leave the tip of the platform_1
            if (self.x >= platform_1['width']) and \
            (self.x <= platform_1['width'] + 1) and \
            (self.y == platform_1['y'] - self.height):
                # let the player free fall
                self.jumpCount = 0
                self.isJump = True

            # free fall at the right edge of the platform_0
            # if it's left edge leave the tip of the platform_0
            elif (self.x >= platform_0['x'] + platform_0['width']) and \
            (self.x <= platform_0['x'] + platform_0['width'] + 1) and \
            (self.y == platform_0['y'] - self.height):
                # let the player free fall
                self.jumpCount = 0
                self.isJump = True
            self.x += self.vel

        # if W key is pressed 
        if keys[pygame.K_w] and self.y > 0:
            self.isJump = True
        
        # if W key is pressed 
        # if keys[pygame.K_w] and self.y > 0: 
            
        #     # set this to True so it's enable the jump_update()
        #     # self.isJump = True
        #     # # decrement in y co-ordinate 
        #     self.y -= self.vel 

        # # if S key is pressed 
        # if keys[pygame.K_s] and self.y < world_y - self.height: 
        #     # increment in y co-ordinate 
        #     self.y += self.vel
            
    # This will render our character - for now it's just a red rectangle
    def render(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

class Platform:
    # rect is (x, y, width, height)
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# print(platform_1['y'])

# Draw the background onto the screen, making sure to scale it to fill the screen
# while preserving the aspect ratio of the image - centers it as well.
background_unscaled = pygame.image.load("images/background_1.png")
def drawBackground(screen):
    bg_res = background_unscaled.get_size()
    screen_res = screen.get_size()
    
    scale_x = screen_res[0] / bg_res[0]
    scale_y = screen_res[1] / bg_res[1]
    best_scale = math.ceil(max(scale_x, scale_y))
    
    scale_res = [
        bg_res[0] * best_scale,
        bg_res[1] * best_scale
    ]

    pos = [
        (screen_res[0] - scale_res[0]) / 2,
        (screen_res[1] - scale_res[1]) / 2,
    ]

    background = pygame.transform.scale(background_unscaled, scale_res)
    screen.blit(background, pos)


def run(screen, start):
    main_character = Player()

    platforms = loadLevel(level_1)

    # rendering loop
    running = True
    while running:
        # determine if we need to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # clear the screen
        screen.fill((0, 0, 0))

        # render the backdrop
        drawBackground(screen)

        # render the level here
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)

        # render the character here
        main_character.render(screen)

        # update the display
        pygame.display.flip()

        # lock the game to 60 fps max
        current_time = time.perf_counter()
        elapsed = current_time - start
        start = current_time
        time.sleep(max(0, (1 / 60) - elapsed))

        # Update the position of the player        
        main_character.update_position(screen, platforms, elapsed)
        main_character.jump_update(platforms, elapsed)