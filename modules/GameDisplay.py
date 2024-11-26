from modules.GameConstants import *
from modules.GameUtility import *
import time

class GameDisplay:
    def __init__(self, game):
        """Initialize hangman display with game reference."""
        self.game = game
        self.images = Paths.hangman_stages
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Hangman Game")

    def loading_screen(self):
        """Display loading screen with progress bar."""
        loading_duration = 2
        start_time = time.time()
        
        warning_font = constants.FONT_SMALL
        warning_lines = [
            "Warning: This game, Hangman,",
            "involves themes of hanging as part of its mechanics,", 
            "intended purely for fun and educational purposes"
        ]
        
        while time.time() - start_time < loading_duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            progress = (time.time() - start_time) / loading_duration
            self.screen.fill(constants.BG_COLOR)
            
            # Warning box positioning
            warning_y = constants.SCREEN_HEIGHT//2 - 200
            line_spacing = 20
            box_padding = 20
            
            rendered_lines = [warning_font.render(line, True, pygame.Color("#FF0000")) for line in warning_lines]
            line_heights = [text.get_height() for text in rendered_lines]
            total_text_height = sum(line_heights) + (line_spacing * (len(warning_lines) - 1))
            
            # Create and draw warning box with padding
            box_height = total_text_height + (box_padding * 2)
            warning_box = pygame.Rect(
                constants.SCREEN_WIDTH//2 - 350,
                warning_y,
                700,
                box_height
            )
            pygame.draw.rect(self.screen, pygame.Color("#FF0000"), warning_box, 2)
            
            current_y = warning_box.centery - (total_text_height // 2)
            
            for i, rendered_text in enumerate(rendered_lines):
                text_rect = rendered_text.get_rect(
                    center=(warning_box.centerx, current_y + (line_heights[i] // 2))
                )
                self.screen.blit(rendered_text, text_rect)
                current_y += line_heights[i] + line_spacing

            # Loading elements
            font = constants.FONT_MEDIUM
            text = font.render("Loading...", True, constants.FONT_COLOR)
            text_rect = text.get_rect(center=(constants.SCREEN_WIDTH//2, warning_box.bottom + 50))
            self.screen.blit(text, text_rect)
            
            bar_width = 400
            bar_height = 20
            bar_rect = pygame.Rect(
                constants.SCREEN_WIDTH//2 - bar_width//2,
                text_rect.bottom + 30,
                bar_width,
                bar_height
            )
            pygame.draw.rect(self.screen, pygame.Color("#333333"), bar_rect)
            
            fill_rect = pygame.Rect(
                bar_rect.left,
                bar_rect.top,
                bar_rect.width * progress,
                bar_height
            )
            pygame.draw.rect(self.screen, constants.BUTTON_COLOR, fill_rect)
            
            percent = f"{int(progress * 100)}%"
            percent_text = font.render(percent, True, constants.FONT_COLOR)
            percent_rect = percent_text.get_rect(center=(constants.SCREEN_WIDTH//2, bar_rect.bottom + 30))
            self.screen.blit(percent_text, percent_rect)
            
            pygame.display.flip()
            self.game.clock.tick(60)

    # In GameDisplay.py, modify start_menu():
    
    def start_menu(self):
        """Draw main menu screen with save functionality."""
        if not pygame.mixer.get_busy():
            self.game.menu_music.play(-1)
    
        self.screen.fill(constants.BG_COLOR)
        
        # Title 
        title_font = constants.FONT_LARGE
        title = title_font.render("HANGMAN", True, constants.FONT_COLOR)
        title_rect = title.get_rect(center=(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT // 2 - 100))
        
        title_border = title_rect.inflate(20, 20)
        pygame.draw.rect(self.screen, constants.FONT_COLOR, title_border, 3)
        
        # Button setup
        button_y_start = constants.SCREEN_HEIGHT // 2 - 50
        button_spacing = 60
        button_width = 200
        button_height = 50
        
        # Create four buttons with proper spacing
        play_button = pygame.Rect(
            constants.SCREEN_WIDTH//2 - button_width//2,
            button_y_start,
            button_width, button_height
        )
        
        continue_button = pygame.Rect(
            constants.SCREEN_WIDTH//2 - button_width//2,
            button_y_start + button_spacing,
            button_width, button_height
        )
        
        restart_button = pygame.Rect(
            constants.SCREEN_WIDTH//2 - button_width//2,
            button_y_start + button_spacing * 2,
            button_width, button_height
        )
        
        quit_button = pygame.Rect(
            constants.SCREEN_WIDTH//2 - button_width//2,
            button_y_start + button_spacing * 3,
            button_width, button_height
        )
        
        self.screen.blit(title, title_rect)
        
        # Draw buttons with different colors
        buttons = [
            (play_button, "PLAY", constants.BUTTON_COLOR),
            (continue_button, "CONTINUE", constants.BUTTON_COLOR),
            (restart_button, "RESTART", constants.BUTTON_COLOR),
            (quit_button, "QUIT", pygame.Color("red"))
        ]
        
        # Check if save file exists to enable/disable continue button
        continue_enabled = self.game.GameState.check_save_exists()
        
        for button, text, color in buttons:
            if text == "CONTINUE" and not continue_enabled:
                color = pygame.Color("#808080")  # Gray out if no save
                
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, constants.FONT_COLOR, button, 3)
            
            button_text = constants.FONT_SMALL.render(text, True, constants.FONT_COLOR)
            self.screen.blit(button_text, button_text.get_rect(center=button.center))
        
        return play_button, continue_button, restart_button, quit_button
    
    
    def draw_hangman(self):
        """Draw hangman state based on attempts."""
        if self.game.attempts < len(self.images):
            self.game.screen.blit(
                self.images[self.game.attempts],  # Use self.images
                (
                    constants.SCREEN_WIDTH // 2 + - constants.width // 2,
                    constants.SCREEN_HEIGHT // 4,
                )
            )


        