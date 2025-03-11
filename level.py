import pygame
import time

def run(screen, start):
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
        pygame.draw.circle(screen, (255, 0, 0), (200, 200), 100)

        # update the display
        pygame.display.flip()

        # sleep for the right amount of time to make the game run at 60 fps
        elapsed = start - time.perf_counter()
        fps_delay = max(0, (1 / 60) - elapsed)
        time.sleep(fps_delay)