import pygame
import time
import math
import json

class Player:
    def __init__(self):
        # our player's absolute position
        self.x = 400
        self.y = 300
        # our player's size
        self.width = 30
        self.height = 40
        # our player's velocity
        self.vel = 10
        # for the jump function
        self.isJump = False
        # this used to adjust the jump height
        self.jumpCount = 7

    # function for jump
    def jump_update(self):
        if self.isJump:
            if self.jumpCount >= -10:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else: 
                self.jumpCount = 10
                self.isJump = False

    # our position is changed based on our velocity
    # Our current velocity is also changed by gravity
    def update_position(self, screen):
        (world_x, world_y) = screen.get_size()

        # stores keys pressed 
        keys = pygame.key.get_pressed() 
        
        # if A key is pressed 
        if keys[pygame.K_a] and self.x > 0: 
            
            # decrement in x co-ordinate 
            self.x -= self.vel
            
        # if D key is pressed 
        if keys[pygame.K_d] and self.x < world_x - self.width: 
            
            # increment in x co-ordinate 
            self.x += self.vel
            
        # if W key is pressed 
        if keys[pygame.K_w] and self.y > 0: 
            
            # set this to True so it's enable the jump_update()
            self.isJump = True
            # # decrement in y co-ordinate 
            # self.y -= self.vel 

        # if S key is pressed 
        if keys[pygame.K_s] and self.y < world_y - self.height: 
            # increment in y co-ordinate 
            self.y += self.vel
            
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

test_level = Level([
    Platform((0,  255,   255), (  0, 200, 250, 10)),
    Platform((255,  0,     0), (450, 200, 250, 10)),
    Platform((255,  0,   255), (  0, 400, 250, 10)),
    Platform((255,  255  , 0), (450, 400, 250, 10)),
    Platform((255,  255, 255), (100, 550, 500, 10)),
])

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
        pygame.time.delay(30)

        # Update the position of the player
        elapsed = time.perf_counter() - start
        
        main_character.update_position(screen)
        main_character.jump_update()