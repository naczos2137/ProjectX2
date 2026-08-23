from __future__ import annotations

from typing import Any
import random
from player import Player
from minigames.minigame import MiniGame
from minigames.fake_ai import FakeAi
from minigames.not_one_vote import NotOneVote
from minigames.blind_auction import BlindAuction
from minigames.be_closer import BeCloser
from minigames.never_ever import NeverEver
from minigames.fuck_marry_kill import FuckMarryKill
from minigames.challenge import Challenge
from item import Item

class _GameMode:
    _ALL_GAMEMODES:  list[_GameMode] = []
    def __init__(self, name: str, obj_class: type[MiniGame], chances_added: int):
        self.name: str = name
        self.obj_class: type[MiniGame] = obj_class
        self._chances_added: int = chances_added
        self._chance: int = 25

        _GameMode._ALL_GAMEMODES.append(self)

    @staticmethod
    def get_gamemode() -> _GameMode:
        selected_gamemode: _GameMode = random.choices(
            population=_GameMode._ALL_GAMEMODES, 
            weights=[gamemode._chance for gamemode in _GameMode._ALL_GAMEMODES],
            k=1
            )[0]
        for gamemode in _GameMode._ALL_GAMEMODES:
            if gamemode != selected_gamemode:
                gamemode._chance += gamemode._chances_added
        return selected_gamemode

_GameMode('fake_ai', FakeAi, 2)
_GameMode('not_one_vote', NotOneVote, 1)
_GameMode('blind_auction', BlindAuction, 5)
_GameMode('be_closer', BeCloser, 5)
_GameMode('never_ever', NeverEver, 5)
_GameMode('fuck_marry_kill', FuckMarryKill, 4)
# _GameMode('challenge', Challenge, 2)

ITEMS: dict[str, Item] = { # Zmiana wymaga też zmiany shopItems w lobby.js
    "you_drink": Item("you_drink", 200, lambda buyer_name, target_name: f'{target_name} pije!'),
    "workout_20": Item("workout_20", 400, lambda buyer_name, target_name: f'{target_name} robi 20 pompek/przysiadów!'),
    "everyone_drink": Item("everyone_drink", 500, lambda buyer_name, target_name: f'KAŻDY PIJE!'),
    "question_master": Item("question_master", 500, lambda buyer_name, target_name: f'Odpowiesz na pytanie {buyer_name} = PIJESZ!'),
    "new_rule": Item("new_rule", 999, lambda buyer_name, target_name: f'{buyer_name} wymyśla nową zasade!'),
    "king_title": Item("king_title", 2000, lambda buyer_name, target_name: f'{buyer_name} podaje swój nowy tytuł! Jeśli inaczej się zwrócisz do niego/j to pijesz'),
    "kings_cup_add": Item("kings_cup_add", 400, lambda buyer_name, target_name: f'{buyer_name} dolewa coś do Kings Cup-a'),
    "kings_cup_drink": Item("kings_cup_drink", 2000, lambda buyer_name, target_name: f'{target_name} Pije Kings Cup-a!'),
}

class Game:
    def __init__(self):
        self.drunk: bool = True
        self.players: dict[str, Player] = {}
        self.online_players: dict[str, Player] = {}
        self.current_lvl = "lobby"
        self.game_mode: MiniGame | None = None
        self.buy_history: list[dict[str, str]] = []

    def get_state(self, player_id: str):
        if player_id not in self.online_players:
            self.online_players[player_id] = self.players[player_id]
        state = {
            'lvl': f"/{self.current_lvl}" if player_id in self.players.keys() else "/",
            'players': [{
                "id": player.player_id,
                "name": player.name,
                "avatar": player.avatar,
                "money": player.money,
                "beer": player.new_beers
            } for player in self.online_players.values()],
            'game_state': self.game_mode.get_state(player_id) if self.game_mode else {},
            'buy_history': self.buy_history
        }
        return state

    def set_info(self, player_id: str, game_info: dict[str, Any]):
        if self.game_mode:
            self.game_mode.set_info(player_id, game_info)

    def add_player(self, player_id, name: str, avatar: str):
        self.players[player_id] = Player(player_id, name, avatar)

    def update_player(self, player_id, name: str, avatar: str):
        self.players[player_id].name = name
        self.players[player_id].avatar = avatar

    def buy(self, buyer_id, item, target_id=None):
        buyer = self.players[buyer_id]
        target = self.players.get(target_id, None)
        item = ITEMS[item]
        if buyer.money >= item.price:
            buyer.money -= item.price
            self.buy_history.append({
                'buyer': buyer_id,
                'item': item.get_notification(buyer.name, target.name if target else None),
            })

    def new_round(self):
        for player in self.players.values():
            player.new_beers = 0
        gamemode: _GameMode = _GameMode.get_gamemode()
        self.current_lvl = gamemode.name
        self.game_mode = gamemode.obj_class(self.online_players)
        self.buy_history.clear()

    def finish_round(self):
        self.current_lvl = "lobby"
        self.game_mode = None
        self.online_players.clear()

