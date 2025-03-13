import pygame
import time
#colors
RED =(255,0,0)
def run(screen, start):
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

        # render the level here
        pygame.draw.circle(screen, RED, (200, 200), 100)
        pygame.draw.polygon(screen, RED, [(200, 50), (100, 300), (300, 300)])
        # update the display
        pygame.display.flip()

        # sleep for the right amount of time to make the game run at 60 fps
        elapsed = start - time.perf_counter()
        fps_delay = max(0, (1 / 60) - elapsed)
        time.sleep(fps_delay)

        """Controls!!!!"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pass
        if keys:[pygame.K_DOWN]:
            pass
        if keys:
            pass
        if keys:
            pass