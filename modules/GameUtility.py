import os
import pygame
from modules.GameConstants import *


class Paths:

    wordlist_1 = os.path.join("assets/wordlist", "test.txt")
    with open(wordlist_1, "r") as file:
            WORD_LIST = [line.strip().lower() for line in file]

    hangman_stages = [
            pygame.transform.smoothscale(
                pygame.image.load(f"assets/hangman_image/amogus_{i}.png"), (constants.width, constants.height)
            )
            for i in range(10)
        ]

    
    gameover_fx = pygame.mixer.Sound('assets/sounds/game_over.wav')
    nextlevel_fx = pygame.mixer.Sound('assets/sounds/next_level.wav')
    startmenu_fx = pygame.mixer.Sound('assets/sounds/start_menu.wav')