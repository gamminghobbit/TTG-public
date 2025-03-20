import pygame
import level
import time

width, height = 800, 600

def main():
    # Initialization
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Learning Game")

    # Framerate control and timing
    start = time.perf_counter()
    level.run(screen, start)

    # Cleanup
    pygame.quit()

main()