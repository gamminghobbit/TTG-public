import pygame
import time

world_x = 800
world_y = 600


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
            if self.jumpCount >= -7:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else: 
                self.jumpCount = 7
                self.isJump = False




    # def gvt_influence(self):
    #     if not self.on_the_ground:
    #         vel = 


    # our position is changed based on our velocity
    # Our current velocity is also changed by gravity
    def update_position(self):
        # velocity_scale = 0.01

        # gravity = 0.001 # 0.001 <- turn off gravity for right now
        # self.dy += gravity * elapsed_seconds

        # self.x += velocity_scale * self.dx * elapsed_seconds
        # self.y += velocity_scale * self.dy * elapsed_seconds


        # stores keys pressed 
        keys = pygame.key.get_pressed() 
        
        # if A key is pressed 
        if keys[pygame.K_a] and self.x>0: 
            
            # decrement in x co-ordinate 
            self.x -= self.vel 
            
        # if D key is pressed 
        if keys[pygame.K_d] and self.x<world_x-self.width: 
            
            # increment in x co-ordinate 
            self.x += self.vel 
            
        # if W key is pressed 
        if keys[pygame.K_w] and self.y>0: 
            
            # set this to True so it's enable the jump_update()
            self.isJump = True
            # # decrement in y co-ordinate 
            # self.y -= self.vel 
            
        # if S key is pressed 
        if keys[pygame.K_s] and self.y<world_y-self.height: 
            # increment in y co-ordinate 
            self.y += self.vel 
            


    
    # # looks at the keys that are pressed and changes the velocity of the player
    # #
    # def update_velocity(self, elapsed_seconds):
    #     # keys = pygame.key.get_pressed()
    #     # if keys[pygame.K_UP] and self.y>0:
    #     #     self.dy -= elapsed_seconds
    #     # elif keys[pygame.K_DOWN] and self.y<600-self.height:
    #     #     self.dy += elapsed_seconds
    #     # if keys[pygame.K_RIGHT and self.x<800-self.width]:
    #     #     self.dx += elapsed_seconds
    #     # if keys[pygame.K_LEFT and self.x>0]:
    #     #     self.dx -= elapsed_seconds

    # def cap_velocity(self):
    #     self.dx = max(-1, min(1, self.dx))
    #     self.dy = max(-1, min(1, self.dy))

    # This will render our character - for now it's just a red rectangle
    def render(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

#colors
RED =(255,0,0)




def run(screen, start):
    main_character = Player()

    # background = pygame.image.load("images/background_1.png").convert()
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
        # render the level here
        # render the character here
        main_character.render(screen)

        # update the display
        pygame.display.flip()
        
        # set delay to prevent player moving too fast
        pygame.time.delay(30)

        # Update the position of the player
        # elapsed = start - time.perf_counter()
        # main_character.update_velocity(elapsed)
        # main_character.cap_velocity()
        main_character.update_position()
        main_character.jump_update()
        # """Controls!!!!"""
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     pass
        # if keys[pygame.K_DOWN]:
        #     pass
        # if keys[pygame.K_LEFT]:
        #     pass
        # if keys[pygame.K_RIGHT]:
        #     pass