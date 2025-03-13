import pygame
import time

class Player:
    def __init__(self):
        # our player's absolute position
        self.x = 0
        self.y = 0
        # our player's velocity
        self.dx = 0
        self.dy = 0
    
    # our position is changed based on our velocity
    # Our current velocity is also changed by gravity
    def update_position(self, elapsed_seconds):
        velocity_scale = 0.01

        gravity = 0 # 0.001 <- turn off gravity for right now
        self.dy += gravity * elapsed_seconds

        self.x += velocity_scale * self.dx * elapsed_seconds
        self.y += velocity_scale * self.dy * elapsed_seconds
    
    # looks at the keys that are pressed and changes the velocity of the player
    def update_velocity(self, elapsed_seconds):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.dy -= elapsed_seconds
        elif keys[pygame.K_DOWN]:
            self.dy += elapsed_seconds
        
        if keys[pygame.K_RIGHT]:
            self.dx += elapsed_seconds
        if keys[pygame.K_LEFT]:
            self.dx -= elapsed_seconds

    def cap_velocity(self):
        self.dx = max(-1, min(1, self.dx))
        self.dy = max(-1, min(1, self.dy))

    # This will render our character - for now it's just a red circle
    def render(self, screen):
        center = (self.x, self.y)
        pygame.draw.circle(screen, RED, center, 40)

#colors
RED =(255,0,0)

def run(screen, start):
    main_character = Player()

    background = pygame.image.load("images/background_1.png").convert()
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
        
        # Update the position of the player
        elapsed = start - time.perf_counter()
        main_character.update_velocity(elapsed)
        main_character.cap_velocity()
        main_character.update_position(elapsed)

        """Controls!!!!"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pass
        if keys[pygame.K_DOWN]:
            pass
        if keys[pygame.K_LEFT]:
            pass
        if keys[pygame.K_RIGHT]:
            pass