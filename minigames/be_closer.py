from typing import Any
import random
from minigames.minigame import MiniGame
from player import Player
import time
import requests
from typing import Callable

class BeCloser(MiniGame):
    def __init__(self, players: dict[str, Player]):
        self.QUESTIONS = [
            ('Za ile ruchanie tego pana w dupe przez godzine?\n<img src="/static/minigames/roksa_gej_1.png" width="200">', 300),
            ('Ile bierze najdroższa kurwa w Bydgoszczy za godzinę?\n<img src="/static/minigames/roksa_bydgoszcz_droga.png" width="200">', 800),
            ('Ile trzeba mieć cm by szanowna 50cio letnia kurwa dała Ci 1h za darmo?\n<img src="/static/minigames/roksa_duzy_gratis.png" width="200">', 18),
            ('Za ile ruchanie użytkownika "Dominisia Gej Suczka" w dupe przez godzine?\n<img src="/static/minigames/roksa_gej_2.png" width="200">', 400),
            ('Za trzeba dopłacić pani Miśce za to by się spuściła (stawka godzinowa to 400zł)?\n<img src="/static/minigames/roksa_trans_1.png" width="200">', 100),
            ('Ile zboczona Ania bierze za godzine peggingu?\n<img src="/static/minigames/roksa_1.png" width="200">', 250),
            ('Jaki nr ma ostatni stream z robienia Projekt X?', 14),
            ('Ile % VATu jest na yerba mate?', 7),
            ('Ile jest SCP na głównej polskiej liście (22.03.2026)? (liczy się ilość zajętych numerów, wiele SCP-PL-001 liczy się jako jeden)', 406),
            ('Ile sekund mineło od 1 stycznia 1970 roku 00:00?', int(time.time())),
            ('Ile kcal ma pół litra żóbra?', 210),
            ('Ile kosztuje Frytosize Mieszany 220g w Kebab King (14.03.2026)?', 44),
            ('Ile km ma wisła?', 1047),
            ('Ile wynosi 2^12?', 2**12),
            ('Jaka liczba została wylosowana (1-1000)?', random.randint(1, 1000)),
            ('Ile pieniędzy ma najbogatszy gracz?', max([player.money for player in players.values()])),
            (r'Ile % alkoholu ma soplica czekoladowa wedel?', 15),
            ('Ile osób rekordowo grało na raz w SCP:SL?', 13908),
            ('Ile kosztuje OF Fagaty na rok (22.03.2026)?', 634),
            ('O ile miesięcy Naczos jest starszy od Queen of The Black?', 3),
            ('W którym roku Czuux wrzucił pierwszą piosenke?', 2017),
            ('Ile lat miał Trump kiedy umarł Stalin?', 6),
            ('Ilu było w historii marszałów polskiej armii?', 6),
            ('Kiedy w Polsce ostatecznie zniesiono tytuły szlacheckie?', 1944),
            ('Ile głosów uzyskał Karol Tadeusz Nawrocki w 2 turze wyborów prezydencjich 2025?', 10606877),
            ('Ile jest napalonych kobiet Wrocław online - samotni seniorzy?\n<img src="/static/minigames/reklama_1.png" width="200">', 150),
            ('Ile minut przedłuża seks Start Erotique?\n<img src="/static/minigames/reklama_2.png" width="200">', 55),
            ('Ile części ma skibidi toilet (stan 27.07.2026)?', 79),
            ('Ile kosztują te słuchawki do wykrywania chorób biorezonansem?\n<img src="/static/minigames/lek_sluchawki.png" width="200">', 1300),
            ('Ile kosztuje taki kamień do cipy przyciągający partnerów?\n<img src="/static/minigames/lek_cipojajo.png" width="200">', 333),
            ('Ile kosztuje godzinna sesja zdejmowania klątw?\n<img src="/static/minigames/lek_szaman.png" width="200">', 1099)
        ]

        self.players: dict[str, Player] = players
        self.question: tuple = random.choice(self.QUESTIONS)
        self.guesses: dict[str, int] = {}

        self.finished = False

    def get_state(self, player_id: str):
        game_state = {
            "question": self.question[0],
            "answer": self.question[1],
            "guesses": self.guesses,
        }
        return game_state

    def set_info(self, player_id: str, info: dict[str, Any]):
        if not self.finished:
            if "guess" in info:
                self.guesses[player_id] = int(info["guess"])
                if len(self.guesses) == len(self.players):
                    self.finished = True
                    guesses_sorted = list(self.guesses.items())
                    guesses_sorted.sort(key=lambda x: abs(x[1] - self.question[1]))

                    for guess in guesses_sorted:
                        if abs(guess[1] - self.question[1]) == abs(guesses_sorted[0][1] - self.question[1]):
                            self.players[guess[0]].money += len(self.players) * 50
                        elif self.question[1] * 0.75 > guess[1] or self.question[1] * 1.25 < guess[1]:
                            self.players[guess[0]].new_beers += 1
                            if self.question[1] * 0.25 > guess[1] or self.question[1] * 3 < guess[1]:
                                self.players[guess[0]].new_beers += 1

