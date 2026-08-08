from typing import Any
import random
from player import Player
from minigames.minigame import MiniGame
from minigames.fake_ai import FakeAi
from minigames.not_one_vote import NotOneVote
from minigames.blind_auction import BlindAuction
from minigames.be_closer import BeCloser
from item import Item

ALL_GAME_MODES: dict[str: MiniGame] = {
    'fake_ai': FakeAi,
    'not_one_vote': NotOneVote,
    'blind_auction': BlindAuction,
    'be_closer': BeCloser
}

ITEMS: dict[str, Item] = { # Zmiana wymaga też zmiany shopItems w lobby.js
    "you_drink": Item("you_drink", 200, lambda buyer_name, target_name: f'{target_name} pije!'),
    "workout_20": Item("workout_20", 400, lambda buyer_name, target_name: f'{target_name} robi 20 pompek/przysiadów!'),
    "everyone_drink": Item("everyone_drink", 500, lambda buyer_name, target_name: f'KAŻDY PIJE!'),
    "question_master": Item("question_master", 500, lambda buyer_name, target_name: f'Odpowiesz na pytanie {buyer_name} = PIJESZ!'),
    "new_rule": Item("new_rule", 999, lambda buyer_name, target_name: f'{buyer_name} wymyśla nową zasade!'),
    "king_title": Item("king_title", 2000, lambda buyer_name, target_name: f'{buyer_name} podaje swój nowy tytuł! Jeśli inaczej się zwrócisz do niego/j to pijesz'),
}

class Game:
    def __init__(self):
        self.drunk: bool = True
        self.players: dict[str, Player] = {}
        self.current_lvl = "lobby"
        self.game_mode: MiniGame | None = None
        self.buy_history: list[dict[str, str]] = []

    def get_state(self, player_id: str):
        state = {
            'lvl': f"/{self.current_lvl}" if player_id in self.players.keys() else "/",
            'players': [{
                "id": player.player_id,
                "name": player.name,
                "avatar": player.avatar,
                "money": player.money,
                "beer": player.new_beers
            } for player in self.players.values()],
            'game_state': self.game_mode.get_state(player_id) if self.game_mode else {},
            'buy_history': self.buy_history
        }
        return state

    def set_info(self, player_id: str, game_info: dict[str, Any]):
        if self.game_mode:
            self.game_mode.set_info(player_id, game_info)

    def add_player(self, player_id, name: str, avatar: str):
        self.players[player_id] = Player(player_id, name, avatar)

    def new_round(self):
        for player in self.players.values():
            player.new_beers = 0
        self.current_lvl = random.choice(list(ALL_GAME_MODES.keys()))
        self.game_mode = ALL_GAME_MODES[self.current_lvl](self.players)
        self.buy_history.clear()

    def finish_round(self):
        self.current_lvl = "lobby"
        self.game_mode = None

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