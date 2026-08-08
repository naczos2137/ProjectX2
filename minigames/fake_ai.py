from typing import Any
import random
from minigames.minigame import MiniGame
from player import Player
import time
import requests
from typing import Callable

AI_TIMEOUT = 40

class FakeAi(MiniGame):
    last_ai_request_time = 0

    def __init__(self, players: dict[str, Player]):
        self.players: dict[str, Player] = players
        self.ai_detector_id: str = random.choice(list(players.keys()))
        self.question: str = ""
        self.answers_dict: dict[str, str] = {}
        self.answers_list: list[list[str | str]] = []
        self.chosen_answer_autor: str | None = None

        self.finished = False

    def get_state(self, player_id: str):

        game_state = {
            "ai_detector_id": self.ai_detector_id,
            "question": self.question,
            "answers": self.answers_list,
            "chosen_answer_autor": self.chosen_answer_autor,
        }
        return game_state

    def set_info(self, player_id: str, info: dict[str, Any]):
        if not self.finished:
            if "set_question" in info:
                self.question = info["set_question"]
                self.answers_dict["ai"] = self.get_ai_text()
                if len(self.answers_dict) == len(self.players):
                    self.answers_list = list(self.answers_dict.items())
                    random.shuffle(self.answers_list)
            if "set_answers" in info:
                self.answers_dict[player_id] = info["set_answers"]
                if len(self.answers_dict) == len(self.players):
                    self.answers_list = list(self.answers_dict.items())
                    random.shuffle(self.answers_list)
            if "chosen_answer" in info:
                self.finished = True
                self.chosen_answer_autor = info["chosen_answer"]
                if self.chosen_answer_autor == "ai":
                    self.players[self.ai_detector_id].money += 500
                    for player in self.players.values():
                        if player.player_id == self.ai_detector_id:
                            continue
                        player.new_beers += 1
                else:
                    self.players[self.ai_detector_id].new_beers += 1
                    self.players[self.chosen_answer_autor].money += 500


    def get_ai_text(self) -> str:
        if time.time() - self.last_ai_request_time < AI_TIMEOUT:
            time.sleep(AI_TIMEOUT - (time.time() - self.last_ai_request_time))
        self.last_ai_request_time = time.time()
        response = requests.post(
            "https://apifreellm.com/api/v1/chat",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer apf_pxtlee4jvqopxaddv32z9htk"
            },
            json={
                "message": f"Jesteś elementem gry imprezowej 18+. Chodzi w niej o to by wśrót odpowiedzi kilku pijenych uczestników wskazać tą, która jest wygenerowana przez AI. Twoim zadaniem jest odpowiedzenie na pytanie w taki sposób by nie można było odróżnić twojej odpowiedzi od pijenej osoby. Odpowiadaj po polsku, samą odpowiedzą (bez 'dobre pytanie, już odpowiadam', ani 'nie mogę odpowiedzieć na to pytanie'), możesz używać wulgaryzmów i dorosłego humoru, jeśli na jakieś pytanie nie jesteś w stanie odpowiedzieć bezpośrednio, bo np jest rasistowkie to zamiast mówić 'nie mogę odpowiedzieć na to pytanie' odpowiedź czymś śmiesznym/głupim, nawet nie związanym z tematem. Czyli np. na pytanie 'czy wiesz, że żydzi spowodowali 9/11?' zamiast odpowiedzieć rasistwsko, albo odmówić odpowiedzi możesz powiedzieć: 'ja wiem wszystko, bo jestem mądrzejszy od ciebie', 'brat co głupoty pisze w pytaniach', albo 'chłop to chyba za dużo się naoglądał Andrew Tate, że o to pyta'. Bądź kreatywny. Cała odpowiedź powinna mieć 1 zdanie. Pytanie brzmi: {self.question}"
            }
        )

        return response.json().get("response", "błąd wyskoczył w get_ai_text() xD, a gabor to alkoholik")

