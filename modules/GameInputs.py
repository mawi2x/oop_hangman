import pygame
from modules.GameElements import *
import os

# InputHandler.py
# GameInputs.py
class GameInputs:
    def __init__(self, game):
        self.game = game
        self.GameElements = GameElements(game)
    
    # In GameInputs.py, update handle_menu_input:
    
    # In GameInputs.py, update handle_menu_input:
    
    def handle_menu_input(self, event: pygame.event.Event, play_button: pygame.Rect, 
                         continue_button: pygame.Rect, restart_button: pygame.Rect, 
                         quit_button: pygame.Rect) -> None:
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                self.game.menu_music.stop()
                self.game.GameDisplay.loading_screen()
                self.game.in_menu = False
                self.game.GameState.reset_game(reset_level=True)
                
            elif continue_button.collidepoint(event.pos):
                if self.game.GameState.check_save_exists():
                    self.game.menu_music.stop()
                    # Load progress before showing loading screen
                    if self.game.GameState.load_progress():
                        self.game.GameDisplay.loading_screen()
                        self.game.in_menu = False
                        self.game.GameState.reset_game(reset_level=False)
                    
            elif restart_button.collidepoint(event.pos):
                try:
                    # Write default values
                    with open('game_save.txt', 'w') as file:
                        file.write("1,1")
                    # Immediately load the new values
                    self.game.level = 1
                    self.game.hint_count = 1
                    self.game.menu_music.stop()
                    self.game.GameDisplay.loading_screen()
                    self.game.in_menu = False
                    self.game.GameState.reset_game(reset_level=True)
                except Exception as e:
                    print(f"Error in restart: {e}")


            elif quit_button.collidepoint(event.pos):
                self.game.running = False
    def handle_game_input(self, event: pygame.event.Event) -> None:
        """Handle gameplay input events."""
        if self.game.popup_active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            hint_rect = self.game.button_positions.get("hint")
            if hint_rect and hint_rect.collidepoint(mouse_pos):
                self.GameElements.use_hint()
                return
            
            for letter, rect in self.game.GameElements.button_positions.items():
                if rect.collidepoint(mouse_pos):
                    if letter not in self.game.guesses:
                        self.game.guesses.append(letter)
                        if letter not in self.game.current_word:
                            self.game.attempts += 1
                    if letter in self.game.GameElements.button_positions:
                        del self.game.GameElements.button_positions[letter]
                    break

        elif event.type == pygame.KEYDOWN:
            letter = event.unicode.lower()
            if letter.isalpha() and len(letter) == 1:
                if letter not in self.game.guesses:
                    self.game.guesses.append(letter)
                    if letter not in self.game.current_word:
                        self.game.attempts += 1

    