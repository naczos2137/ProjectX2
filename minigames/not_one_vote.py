from typing import Any
import random
from minigames.minigame import MiniGame
from player import Player
import time
import requests
from typing import Callable

class NotOneVote(MiniGame):
    def __init__(self, players: dict[str, Player]):
        self.players: dict[str, Player] = players
        self.player_his_vote: dict[str, str] = {}
        self.player_votes_on_him: dict[str, int] = {player_id: 0 for player_id in players.keys()}

        self.finished = False

    def get_state(self, player_id: str):

        game_state = {
            "votes": self.player_votes_on_him,
        }
        return game_state

    def set_info(self, player_id: str, info: dict[str, Any]):
        if not self.finished:
            if "vote" in info:
                self.player_his_vote[player_id] = info["vote"]

                if len(self.player_his_vote) == len(self.players):
                    self.finished = True

                    for voter, votes in self.player_his_vote.items():
                        self.player_votes_on_him[votes] += 1

                    for player_id, votes in self.player_votes_on_him.items():
                        if votes == 1:
                            self.players[player_id].new_beers += 1
                        else:
                            self.players[player_id].money += 100
