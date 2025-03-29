import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player properties
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_STRENGTH = -14

# Platform properties
PLATFORM_THICKNESS = 24

# --- Game States ---
STATE_PLAYING = 0
STATE_QUESTION = 1
STATE_GAME_OVER = 2
STATE_WIN = 3

# --- Questions ---
# Format: (Question text, [Option 1, Option 2, Option 3, Option 4], Correct Option Index (0, 1, 2, or 3))
QUESTIONS = [
    ("What color is the sky on a clear day?", ["Beige", "Green", "Red", "Blue"], 3),
    ("How many legs does a spider typically have?", ["6", "8", "10", "12"], 1),
    ("What is 2 + 2?", ["3", "4", "5", "2"], 1),
    ("Which planet is known as the Red Planet?", ["Earth", "Mars", "Jupiter", "Pluto"], 1),
    ("What is the main ingredient in bread?", ["Sugar", "Flour", "Salt", "Cocaine"], 1)
]

# --- Helper Functions ---
def draw_text(surface, text, size, x, y, color=WHITE, font_name=None):
    """Helper function to draw text on the screen."""
    if font_name is None:
        font_name = pygame.font.match_font('arial') # Find a default system font
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# --- Game Class ---
class Game:
    def __init__(self):
        """Initialize Pygame, screen, clock, and game variables."""
        pygame.init()
        # pygame.mixer.init() # For sound effects later
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer with Questions")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = STATE_PLAYING
        self.font_name = pygame.font.match_font('arial')

        # Question related variables
        self.questions_to_ask = random.sample(QUESTIONS, 3) # Pick 3 random Qs
        self.current_question_index = -1 # Start before the first question
        self.questions_answered_correctly = 0
        self.total_questions_asked = 0
        self.active_question_data = None # Stores current question details
        self.question_feedback = "" # To show "Correct!" or "Wrong!"

        self.load_data()

    def load_data(self):
        """Load game assets and set up initial game state."""
        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # Player
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Platforms (Create some platforms)
        platform_positions = [
            (0, SCREEN_HEIGHT - PLATFORM_THICKNESS, SCREEN_WIDTH, PLATFORM_THICKNESS), # Ground
            (150, SCREEN_HEIGHT - 100, 200, PLATFORM_THICKNESS),
            (450, SCREEN_HEIGHT - 200, 150, PLATFORM_THICKNESS),
            (200, SCREEN_HEIGHT - 350, 180, PLATFORM_THICKNESS),
            (600, SCREEN_HEIGHT - 450, 150, PLATFORM_THICKNESS)
        ]

        for pos in platform_positions:
            p = Platform(*pos)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # Goal
        self.goal_rect = pygame.Rect(700, SCREEN_HEIGHT - 450 - 30, 50, 30) # Place it near the last platform

    def run(self):
        """The main game loop."""
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0 # Delta time in seconds
            self.events()
            if self.game_state == STATE_PLAYING:
                self.update()
                self.draw()
            elif self.game_state == STATE_QUESTION:
                # Don't update game physics, just handle question input
                self.draw() # Draw game behind question
                self.draw_question_screen() # Draw question overlay
            elif self.game_state == STATE_WIN:
                self.draw()
                self.draw_win_screen()
            elif self.game_state == STATE_GAME_OVER: # Could add a losing state later
                self.draw()
                self.draw_game_over_screen() # Placeholder if needed

            pygame.display.flip() # Update the full display Surface to the screen

        pygame.quit()
        sys.exit()

    def update(self):
        """Update game logic (player movement, collisions)."""
        # Update all sprites (this calls Player.update() which calculates new pos/vel)
        self.all_sprites.update()

        # --- Player Platform Collision Handling ---
        # Check for collisions *after* player position is updated

        # Vertical collisions (Landing on platforms)
        if self.player.vel.y > 0:  # Check collisions only when falling downward
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # Find the highest platform the player has collided with
                # This is the one with the smallest 'top' y-coordinate
                landing_platform = min(hits, key=lambda p: p.rect.top)

                # Check if the player's bottom edge actually passed the platform's top edge
                # This prevents snapping upwards if hitting the side of a platform while rising
                # or if slightly overlapping horizontally without landing.
                # We only correct position if the player is truly landing on top.
                # A common check is if the player's *previous* bottom was above the platform top.
                # Simpler approach: If falling (vel.y > 0) and colliding, assume landing for now.

                # Correct player position: Snap the player's bottom to the platform's top
                # Ensure player doesn't fall through thin platforms if moving very fast:
                if self.player.rect.bottom > landing_platform.rect.top:
                    self.player.rect.bottom = landing_platform.rect.top
                    # Crucially, update the underlying position vector to match the snapped rect
                    self.player.pos.y = self.player.rect.midbottom[1]
                    self.player.vel.y = 0  # Stop vertical movement
                    self.player.is_jumping = False  # Allow jumping again

        # --- End Player Platform Collision Handling ---

        # Check for goal collision - only if enough questions answered correctly
        if self.questions_answered_correctly >= 3:
            if self.player.rect.colliderect(self.goal_rect):
                self.game_state = STATE_WIN

        # Keep player on screen horizontally (simple boundary)
        if self.player.rect.right > SCREEN_WIDTH:
            self.player.rect.right = SCREEN_WIDTH
            self.player.pos.x = self.player.rect.centerx
            self.player.vel.x = 0 # Stop horizontal movement at edge
        if self.player.rect.left < 0:
             self.player.rect.left = 0
             self.player.pos.x = self.player.rect.centerx
             self.player.vel.x = 0 # Stop horizontal movement at edge

        # Check if player falls off screen bottom (Reset)
        # This check remains as a fallback if something goes wrong or
        # if there are gaps without platforms at the bottom.
        if self.player.rect.top > SCREEN_HEIGHT:
            # Simple reset for now, could implement lives or game over
            self.player.pos = pygame.math.Vector2(100, SCREEN_HEIGHT - 100) # Start near bottom left-ish
            self.player.vel = pygame.math.Vector2(0, 0)
            self.player.acc = pygame.math.Vector2(0, 0)
            self.player.rect.midbottom = self.player.pos # Reset rect position too

    def events(self):
        """Handle events (keyboard input, quitting)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_q:
                        # Check if there are more questions to ask
                        if self.total_questions_asked < len(self.questions_to_ask):
                            self.ask_next_question()
                elif self.game_state == STATE_QUESTION:
                    if event.key == pygame.K_1:
                        self.check_answer(0)
                    elif event.key == pygame.K_2:
                        self.check_answer(1)
                    elif event.key == pygame.K_3:
                         self.check_answer(2)
                    elif event.key == pygame.K_4:
                         self.check_answer(3)
                    # Allow returning to game even if question not answered (optional)
                    # if event.key == pygame.K_ESCAPE:
                    #    self.game_state = STATE_PLAYING
                    #    self.active_question_data = None
                elif self.game_state == STATE_WIN or self.game_state == STATE_GAME_OVER:
                     if event.key == pygame.K_r: # Restart game
                         self.__init__() # Re-initialize the game object
                         self.run() # Start the loop again
                     if event.key == pygame.K_ESCAPE:
                         self.running = False


    def draw(self):
        """Draw everything to the screen."""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Draw the goal only if enough questions are answered
        goal_color = YELLOW if self.questions_answered_correctly >= 3 else (100, 100, 0) # Dim if inactive
        pygame.draw.rect(self.screen, goal_color, self.goal_rect)

        # Draw HUD (Score/Questions Answered)
        draw_text(self.screen, f"Correct Answers: {self.questions_answered_correctly} / {len(self.questions_to_ask)}",
                  18, SCREEN_WIDTH / 2, 10, WHITE)
        if self.total_questions_asked < len(self.questions_to_ask):
            draw_text(self.screen, "Press Q to answer next question", 18, SCREEN_WIDTH / 2, 35, WHITE)
        elif self.questions_answered_correctly < len(self.questions_to_ask):
             draw_text(self.screen, "Not enough correct answers to finish!", 18, SCREEN_WIDTH / 2, 35, RED)
        else:
             draw_text(self.screen, "Goal is active! Reach the yellow box!", 18, SCREEN_WIDTH / 2, 35, YELLOW)


    def ask_next_question(self):
        """Prepare and switch to the question state."""
        if self.total_questions_asked < len(self.questions_to_ask):
            self.current_question_index = self.total_questions_asked # Use total asked as index
            self.active_question_data = self.questions_to_ask[self.current_question_index]
            self.game_state = STATE_QUESTION
            self.question_feedback = "" # Clear previous feedback

    def check_answer(self, selected_option_index):
        """Check the player's answer and provide feedback."""
        if self.active_question_data:
            _, _, correct_index = self.active_question_data
            if selected_option_index == correct_index:
                self.questions_answered_correctly += 1
                self.question_feedback = "Correct!"
            else:
                self.question_feedback = "Wrong!"

            self.total_questions_asked += 1
            self.active_question_data = None # Mark question as handled

            # Optionally, add a small delay before returning to game
            pygame.time.wait(1000) # Wait 1 second to show feedback

            self.game_state = STATE_PLAYING


    def draw_question_screen(self):
        """Draw the question and options overlay."""
        if not self.active_question_data:
             # If we are in question state but no active question (e.g. during feedback)
             # Still draw the feedback if any
             if self.question_feedback:
                  overlay = pygame.Surface((SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.5))
                  overlay.set_alpha(200) # Make it semi-transparent
                  overlay.fill(BLACK)
                  rect = overlay.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                  self.screen.blit(overlay, rect.topleft)
                  draw_text(self.screen, self.question_feedback, 40, SCREEN_WIDTH / 2, rect.top + 50, GREEN if "Correct" in self.question_feedback else RED)
             return # Exit if no question data

        question_text, options, _ = self.active_question_data

        # Draw a semi-transparent background for the question box
        overlay = pygame.Surface((SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.6)) # Adjust size as needed
        overlay.set_alpha(220) # Make it semi-transparent
        overlay.fill(BLACK)
        rect = overlay.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(overlay, rect.topleft)

        # Draw Question Text
        draw_text(self.screen, question_text, 28, SCREEN_WIDTH / 2, rect.top + 30, WHITE)

        # Draw Options
        option_y_start = rect.top + 100
        option_spacing = 50
        for i, option in enumerate(options):
            option_text = f"{i+1}. {option}"
            draw_text(self.screen, option_text, 22, SCREEN_WIDTH / 2, option_y_start + i * option_spacing, WHITE)

        # Draw Instructions
        draw_text(self.screen, "Press number key (1, 2, 3, or 4) to answer", 18, SCREEN_WIDTH / 2, rect.bottom - 30, YELLOW)


    def draw_win_screen(self):
        """Display the win message."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, "YOU WIN!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, GREEN)
        draw_text(self.screen, "You answered enough questions correctly!", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, WHITE)
        draw_text(self.screen, "Press R to Play Again or ESC to Quit", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, WHITE)

    def draw_game_over_screen(self):
         """Display the game over message (placeholder)."""
         # This state isn't fully used in this version, but could be expanded
         overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
         overlay.set_alpha(180)
         overlay.fill(BLACK)
         self.screen.blit(overlay, (0, 0))
         draw_text(self.screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, RED)
         draw_text(self.screen, "Press R to Play Again or ESC to Quit", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, WHITE)


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game # Reference to the main game object
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        # Using vectors for position, velocity, acceleration
        self.pos = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.is_jumping = False

    def jump(self):
        """Make the player jump, but only if standing on a platform."""
        # Check if standing on a platform first
        self.rect.y += 1 # Move down 1 pixel to check for platform below
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1 # Move back up

        if hits and not self.is_jumping: # Only jump if on ground
            self.vel.y = PLAYER_JUMP_STRENGTH
            self.is_jumping = True

    def update(self):
        """Update player physics (movement, gravity)."""
        # Reset acceleration
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)

        # Handle key presses for horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # Equations of motion (Euler integration)
        self.vel += self.acc
        # Limit horizontal speed if needed:
        # MAX_SPEED = 5
        # if abs(self.vel.x) > MAX_SPEED:
        #     self.vel.x = MAX_SPEED if self.vel.x > 0 else -MAX_SPEED

        self.pos += self.vel + 0.5 * self.acc # Improved position update

        # Update rect center based on position vector
        self.rect.midbottom = self.pos # Align bottom of rect with position vector

        # Collision detection happens in the main game update loop after movement

# --- Platform Class ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- Start the Game ---
if __name__ == "__main__":
    game = Game()
    game.run()
