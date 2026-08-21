from typing import Any
import random
from minigames.minigame import MiniGame
from player import Player
import time
import requests
from typing import Callable

TASKS = [
    'Zrób 20 pompek',
    'Szot czystej',
    'Walnij fikołka',
    'Zrób fikołka do tyłu',
    'Wyślij do kogoś z bliskiej rodziny: "Jestem gejem"',
    'Zrób 25 przysiadów',
    'Zrób 50 brzuszków',
    'Idź dotknąć trawy',
    'Tańcz przez około 30s:\n<img src="/static/minigames/fortnite1.gif" width="200">',
    'Tańcz przez około 30s:\n<img src="/static/minigames/fortnite2.gif" width="200">',
    'Tańcz przez około 30s:\n<img src="/static/minigames/fortnite3.gif" width="200">',
    'Zatwierkuj',
    'Zmień się 1 częścią ubrania z osobą na 2 miejscu',
    'Wymyśl (nie może być istniejąca) teorie sposkową i na freestajlu zacznij wszystkich do niej przekonywać, odpowiedź na wszystkie pytania do niej, cały czas wyglądaj na śmiertelnie poważnego',
    'Wyślij to do ostatniej osoby na Messengerze (podczas licytacji nie możesz sprawdzać kto to jest): \n<img src="/static/minigames/never_give_up.png" width="200">',
    'Zjedź łyżeczkę cukru',
    'Zrób 1 minutę planka',
    'Zaśpiewaj karaoke piosenki wybranej przez osobę na 2 miejscu (piosenka musi być znana przez innych)',
    'Zrób freestyle disstrack na osobę na ostatnim miejscu',
    'Wypij shota zrobionego przez osobę na 2 miejscu',
]

class BlindAuction(MiniGame):
    def __init__(self, players: dict[str, Player]):
        self.players: dict[str, Player] = players
        self.task: str = random.choice(TASKS)
        self.bids: dict[str, int] = {}

        self.finished = False

    def get_state(self, player_id: str):
        game_state = {
            "task": self.task,
            "bids": self.bids,
        }
        return game_state

    def set_info(self, player_id: str, info: dict[str, Any]):
        if not self.finished:
            if "bid" in info:
                self.bids[player_id] = int(info["bid"])
                if len(self.bids) == len(self.players):
                    self.finished = True
                    bids_sorted = list(self.bids.items())
                    bids_sorted.sort(key=lambda x: x[1])

                    self.players[bids_sorted[0][0]].money += bids_sorted[0][1]
                    self.players[bids_sorted[-1][0]].new_beers += 1

