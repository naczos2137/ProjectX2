from typing import Any
import random

from minigame import MiniGame
from player import Player

TASKS = [
    ("Zdejmij 1 część ubrania", (1)),
    ("Zdejmij skarpetki", (1)),
    ("Powiedź kiedy ostatnio uprawiałeś seks", (1)),
    ("Kiss or slap {random_player}", (1)),
    ("Daj klapsa wybranej przez Ciebie osobie", (1)),
    ("Wymyśl 1 nigdy-przenigdy", (1)),
    ("Zrób 25 brzuszków", (1)),
    ("Wymień 1 negatywną cechę {random_player}", (1)),
    ("Zamieńcie się 1 częścią ubrania", (2)),
    ("Kamień papier nożyce. Przegrany pije", (2)),
    ("Stań na 1 nodze. Ostatnia osoba pije", (3,4,5)),
    ("Podłoga to lawa!. Ostatnia osoba pije", (3,4,5)),
]

class Challenge(MiniGame):
    def __init__(self, players: dict[str, Player]):
        self.players: dict[str, Player] = players

        self.finished = False

    def get_state(self, player_id: str):
        game_state = {
            
        }
        return game_state

    def set_info(self, player_id: str, info: dict[str, Any]):
        if not self.finished:
            pass

