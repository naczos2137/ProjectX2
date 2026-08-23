from typing import Any
import random

from minigames.minigame import MiniGame
from player import Player

TASKS = [
    ("Zdejmij 1 część ubrania", (1,)),
    ("Zdejmij skarpetki", (1,)),
    ("Powiedź kiedy ostatnio uprawiałeś seks", (1,)),
    ("Powiedź kiedy ostatnio robiłeś sobie dobrze", (1,)),
    ("Kiss or slap {random_player}", (1,)),
    ("Daj klapsa wybranej przez Ciebie osobie", (1,)),
    ("Zrób 25 brzuszków", (1,)),
    ("Zrób 10 bułgarów", (1,)),
    ("Wymień 1 negatywną cechę {random_player}", (1,)),
    ("Wymieńcie się piciem", (2,)),
    ("Zamieńcie się 1 częścią ubrania", (2,)),
    ("Kamień papier nożyce. Przegrany pije", (2,)),
    ("Stań na 1 nodze. Ostatnia osoba pije", (3,4,5)),
    ("Podłoga to lawa!. Ostatnia osoba pije", (3,4,5)),
]

class Challenge(MiniGame):

    def __init__(self, players: dict[str, Player]):
        self.players = players

        player_count = len(players)

        possible_tasks = []

        for task, valid_counts in TASKS:
            if player_count in valid_counts:
                possible_tasks.append((task, valid_counts))

        self.task, valid_counts = random.choice(possible_tasks)

        self.selected_players = random.sample(
            list(players.keys()),
            k=random.choice(valid_counts)
        )

        random_player = self.players[
            random.choice(list(players.keys()))
        ].name

        self.task = self.task.replace(
            "{random_player}",
            random_player
        )

        for player_id in self.selected_players:
            self.players[player_id].money += 100

        self.finished = False

    def get_state(self, player_id: str):
        return None

    def set_info(self, player_id: str, info):
        return None