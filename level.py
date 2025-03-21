import pygame
import time
import math
import json

window_x = 800
window_y = 600

class Player:
    def __init__(self):
        # our player's absolute position
        self.x = 0
        self.y = 600-40
        # our player's size
        self.width = 30
        self.height = 40
        # our player's velocity
        self.vel = 5
        # for the jump function
        self.isJump = False
        # this is used to adjust the jump height
        self.default_jumpCount = 25
        self.jumpCount = self.default_jumpCount


    # function for jump and collision detect
    def jump_update(self):
        if self.isJump:
            # if self.jumpCount >= -40:
            if not self.y + self.height > window_y:
                if (self.y < test_level.platform_list[4].rect[1] + 20) and (self.y + self.height >= test_level.platform_list[4].rect[1] + 20) and (self.x <= test_level.platform_list[4].rect[0] + test_level.platform_list[4].rect[2]) and (self.x + self.width >= test_level.platform_list[4].rect[0]):
                    self.jumpCount = 0
                    self.y = test_level.platform_list[4].rect[1] + 20

                elif (self.y < test_level.platform_list[2].rect[1] + 20) and (self.y + self.height >= test_level.platform_list[2].rect[1] + 20) and (self.x <= test_level.platform_list[2].rect[2]):
                    self.jumpCount = 0
                    self.y = test_level.platform_list[2].rect[1] + 20

                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.04 # this 0.00.. is used to control the jump speed, and it will influence the jump height too
                self.jumpCount -= 1

                if (self.y <= test_level.platform_list[2].rect[1]) and (self.y + self.height >= test_level.platform_list[2].rect[1]) and (self.x <= test_level.platform_list[2].rect[2]):
                    self.y = test_level.platform_list[2].rect[1] - self.height
                    self.jumpCount = self.default_jumpCount
                    self.isJump = False
                elif (self.y <= test_level.platform_list[4].rect[1]) and (self.y + self.height >= test_level.platform_list[4].rect[1]) and (self.x <= test_level.platform_list[4].rect[0] + test_level.platform_list[4].rect[2]) and (self.x + self.width >= test_level.platform_list[4].rect[0]):
                    self.y = test_level.platform_list[4].rect[1] - self.height
                    self.jumpCount = self.default_jumpCount
                    self.isJump = False

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
    def update_position(self, screen):
        (self.world_x, self.world_y) = screen.get_size()

        # stores keys pressed 
        keys = pygame.key.get_pressed() 
        
        # if A key is pressed 
        if keys[pygame.K_a] and self.x > 0: 
            
            if  (self.x + self.width <= test_level.platform_list[4].rect[0]) and (self.x + self.width >= test_level.platform_list[4].rect[0] - 1) and (self.y == test_level.platform_list[4].rect[1] - self.height):
                self.jumpCount = 0
                self.isJump = True
            # decrement in x co-ordinate 
            self.x -= self.vel
            
        # if D key is pressed 
        if keys[pygame.K_d] and self.x < self.world_x - self.width: 

            if (self.x >= test_level.platform_list[2].rect[2]) and (self.x <= test_level.platform_list[2].rect[2] + 1) and (self.y == test_level.platform_list[2].rect[1] - self.height):
                self.jumpCount = 0
                self.isJump = True
            elif (self.x >= test_level.platform_list[4].rect[0] + test_level.platform_list[4].rect[2]) and (self.x <= test_level.platform_list[4].rect[0] + test_level.platform_list[4].rect[2] + 1) and (self.y == test_level.platform_list[4].rect[1] - self.height):
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

class Level:
    def __init__(self, platform_list):
        self.platform_list = platform_list
    
    def render_platforms(self, screen):
        for platform in self.platform_list:
            pygame.draw.rect(screen, platform.color, platform.rect)


#colors
RED = (255, 0, 0)

# rect is (x, y, width, height)
test_level = Level([
    Platform((0,  255,   255), (  0, 200, 250, 20)),
    Platform((255,  0,     0), (450, 200, 250, 20)),
    Platform((255,  0,   255), (  0, 400, 250, 20)),
    Platform((255,  255  , 0), (450, 400, 250, 20)),
    Platform((255,  255, 255), (200, 530, 500, 20)),
])

print(test_level.platform_list[2].rect[1])

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
        test_level.render_platforms(screen)

        # render the character here
        main_character.render(screen)

        # update the display
        pygame.display.flip()
        
        # set delay to prevent player moving too fast
        # pygame.time.delay(30)

        # Update the position of the player
        elapsed = time.perf_counter() - start
        
        main_character.update_position(screen)
        main_character.jump_update()