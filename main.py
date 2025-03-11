import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball")

# Set up the clock for framerate control hihudha
clock = pygame.time.Clock()

# Ball properties
ball_radius = 20
ball_color = (255, 0, 0)  # Red
ball_x = width // 2
ball_y = height // 2
ball_dx = 5  # Horizontal velocity
ball_dy = 3  # Vertical velocity

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce off the left and right walls
    if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
        ball_dx = -ball_dx

    # Bounce off the top and bottom walls
    if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
        ball_dy = -ball_dy

    # Clear the screen (fill with black)
    screen.fill((0, 0, 0))

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
