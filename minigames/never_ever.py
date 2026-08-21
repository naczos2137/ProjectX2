from typing import Any, Optional
import random

from minigames.minigame import MiniGame
from player import Player

QUESTIONS = {
    "SEX": [
        "uprawiałem seksu",
        "uprawiałem seksu w miejscu publicznym",
        "uprawiałem seksu z osobą they/them (lub inne niestandardowe)",
        "uprawiałem seksu w zamian za coś (w obie strony się liczy)",
        "uprawiałem seksu z 2 osobami naraz",
        "uprawiałem seksu z osobą, która uprawiała wcześniej/później seks z moim bliskim znajomym",
        "uprawiałem seksu z ex",
        "uprawiałem seksu z kimś kto był w otwartym związku",
        "lizałem się z ex",
        "miałem one night standa",
        "patrzyłem jak ktoś uprawia seks",
        "zostałem przyłapany na seksie",
        "przyłapałem kogoś na seksie",
        "słyszałem przez ścianę jak ktoś z rodziny uprawiał seks",
        "plunąłem nikomu w twarz podczas seksu",
        "plunął mi nikt w twarz podczas seksu",
        "byłem związany podczas seksu",
        "związałem kogoś podczas seksu",
        "grałem w gry komputerowe podczas gdy ktoś uprawiał seks w tym samym pokoju",
        "uprawiałem seksu bez zabespieczenia",
        "pękła mi/partnetowi guma podczas seksu",
        "robiłem/dostawałem footjoba",
        "robiłem/dostawałem titjoba",
        "siedział mi nikt nago na twarzy",
        "siedziałem komuś nago na twarzy",
        "robiłem 69",
        "lizałem fiuta",
        "lizałem cipę",
        "robiłem analu",
        "całowałem się z trans",
        "całowałem się z 2  osobami na raz",
        "całowałem się z minimum 3 osobami na 1 imprezie",
        "miałem w sobie dildo",
        "używałem sztucznej cipy/huja",
        "zapłaciłem za porno",
        "wysłałem nikomu swoich nagich zdjęć",
        "robiłem sobię dobrze do gejowskiego porno",
        "robiłem sobie dobrze do pissing porno",
        "podglądałem kogoś nago",
        "robiłem sobie dobrze do zdjęć osoby z klasy",
        "robiłem sobie dobrze w szkole",
        "robiłem sobie dobrze z przynajmniej 4 osobami w tym samym pokoju",
        "robiłem sobie dobrze jedzeniem",
        "jadłem spermy",
        "byłem w strip clubie",
        "całowałem się z kimś nie znając jego imienia",
        "robiłem sobie dobrze w tym tygodniu"
    ],
    "UŻYWKI (do włosów)": [
        "piłem bimbru",
        "wypiłem szot alkoholu mocniejszego niż 90%",
        "piłem alkoholu przed 15 rokiem życia (przynajmniej pół piwa)",
        "byłem pijany przed 18 rokiem życia",
        "wymiotowałem od alkoholu",
        "zażygałem ubera",
        "żygałem w ToiToju"
        "prowadziłem pijany",
        "wypiłem 0.5l alko 40% w mniej niż 30min",
        "wyzerowałem piwa na raz",
        "odmówiono mi sprzedaży alkoholu, bo byłem zbyt pijany",
        "nie wpuszczono mnie do klubu, bo byłem zbyt pijany",
        "wypaliłem paczki papierosów w dobę",
        "wymiotowałem po nikotynie",
        "brałem snusa",
        "wciągałem tabaki",
        "paliłem zioła",
        "waliłem wiadra (irl, nie w mc)",
        "jadłem ciastek z ziołem",
        "jadłem grzybków",
        "brałem czegoś mocniejszego od zioła",
        "mieszałem psychotropów z alkoholem",
        "mieszałem psychotropów z ziołem",
        "byłem w kasynie",
        "straciłem na raz więcej niż 100zł w hazardzie",
        "postawiłem na zielone w kasynie irl",
        "grałem w lotto",
        "otwierałem skrzynek w CS:GO",
        "miałem w 1 grze więcej niż 2k godzin",
        "wydałem na skiny do 1 gry więcej niż 500zł",
        "zrobiłem nocki na granie, a rano poszedłem do szkoły/pracy",
        "grałem 8h ciągiem",
        "wydałem więcej niż 5k zł na raz na elektronike"
    ],
    "BANDYTERKA": [
        "dostałem nagany w szkole",
        "uciekłem z domu na przynejmniej 12h",
        "ukradłem pieniędzy rodzicom z portfela",
        "przekroczyłem prędkości o ponad 50km/h",
        "byłem spisywany przez policję",
        "składałem zeznań na policji",
        "dzwoniłem na numer alarmowy",
        "przyjechała do mnie do domu policja",
        "kupowałem narkotyków od dilera",
        "spiraciłem gry",
        "nigdy się nie ciołem",
        "rysowałem graffiti",
    ],
    "ŻYCIE": [
        "przeczytałem całej książki w tym roku",
        "miałem na sobię full makeup",
        "miałem pomalowanych paznokci",
        "byłem w czołgu",
        "postawiono mi drinka w barze (przez nieznajomego)",
        "zapytałem o numer/ig nieznajomej osoby i mi go dała (w sensie rizz irl)",
        "zapytałem o numer/ig nieznajomej osoby i mi go nie dała (w sensie rizz irl)",
        "byłem w azji",
        "byłem w afryce",
        "byłem poza eu",
        "miałem karty kredytowej",
        "wziołem pożyczki",
        "kupiłem niczego na raty",
        "byłem w związku przynejmniej 2 lata",
        "zerwał ze mną nikt przez SMSa (discord/messenger/itp)",
        "byłem w situationshipie",
        "nie używałem telefonu przez tydzień (po 15 roku życia)",
        "dzwoniłem pijany do ex",
        "byłem na urbexie",
        "byłem na youtubie",
        "jeździłem na koniu",
        "miałem tindera",
        "byłem na proteście",
        "powiedziałem n-worda",
        "podałem ręki czarnuchowi",
        "podałem ręki żydowi",
        "przytuliłem ukraińca",
        "przytuliłem białorusina",
        "nagrałem piosenki",
        'łowiłem ryb'
    ]
}

class NeverEver(MiniGame):
    def __init__(self, players: dict[str, Player]):
        self.players: dict[str, Player] = players
        self.selector_id: str = random.choice(list(players.keys()))
        self.categories: list[str] = random.sample(list(QUESTIONS.keys()), 2)
        self.question: Optional[str] = None

        self.finished = False

    def get_state(self, player_id: str):
        game_state = {
            "selector": self.selector_id,
            "categories": self.categories,
            "question": self.question
        }
        return game_state

    def set_info(self, player_id: str, info: dict[str, Any]):
        if not self.finished:
            if "category" in info and self.question == None:
                self.question = random.choice(QUESTIONS[info["category"]])
