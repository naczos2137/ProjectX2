from typing import Any
import random

from minigames.minigame import MiniGame
from player import Player

PERSONS: dict[str, dict[int, list[str]]] = {
    'male': {
        1: [
            'Jarosław Kaczyński',
            'Zbigniew Stonoga',
            'Mariusz Trynkiewicz',
            'Janusz Korwin Mikke',
            'Grzegorz Braun',
            'Donald Tusk',
            'Jeffery Epstein',
            'Lech Kaczyński',
            'Ted Kaczyński (Unabomber)',
            'George Floyd (czarnuch)',
            'Beniamin Natanyahu (Big Yahoo)',
            'Adolf Hitler',
            'Józef Stalin',
            'Bill Clinton',
            'Joe Biden',
            'Judasz',
            'Christine Weston Chandler',
            'Speed z Zootopii',
        ],
        2: [
            'Charlie Kirk',
            'Stuart Burton (Stuu)',
            'Michał Baron (Boxdel)',
            'Wołodymir Załeński',
            'Pan Tadeusz',
            'Stanisław Wokulski',
            'Jacek Kaczmarski',
            'Tinky Winky',
            'Tim Deen',
            'Józef Piłsudski',
            'Max Verstappen',
            'Freddy Fazbear ',
            'Michael Myers',
            'I Show Speed',
        ],
        3: [
            'Janusz Grad',
            'Krzysztof Bosak',
            'Gerald z Rivii',
            'Hubert Moszka',
            'Robert Lewandowski',
            'Taconafide',
            'Święty Mikołaj',
            'Kacper Błoński',
            'Johny Sins',
            'Keanu Reeves',
            'Arnold Schwarzenegger',
            'Markiplier',
            'Mr. Beast',
            'Erling Haaland',
            'Harry Potter',
            'Ghostface',
        ]
    },
    'female': {
            1: [
                'Magda Gessler',
                'Anna Grocka',
                'Godlewska',
                'Beata Szydło',
                'Margaret Thacher',
                'Olivka Brasil',
                'Dorota Wellman',
                'Halina Kiepska',
                'Madonna',
                'Maryla Rodowicz',
                'Greta Thunberg',
                'GLaDOS',
            ],
            2: [
                'Izabela Łęcka',
                'Anna Frank',
                'Fagata',
                'Seksmasterka',
                'Bonnie Blue',
                'Lily Phillips'
                'Sasha Grey',
                'Ice Spice',
                'Sweetie Fox',
                'Eva Elfie',
                'Mia Malkova',
                'Adriana Chechik',
                'Belle Delphine',
                'Ewa Hodakowska',
                'Fretka z Fineasha i Ferba',
                'Velma z Scooby Doo',
                'Toy Chicka',
            ],
            3: [
                'Anna Lewandowska',
                'Young Leosia',
                'Queen of the Black',
                'Roksana Węgiel',
                'Britney Spears',
                'Hannah Montana',
                'Billie Eilish',
                'Sydney Sweeney',
                'Ewa Swoboda',
                'Kim Kolwiek',
                'Lara Croft',
                'Daphne z Scooby Doo',
                'Lola z Królika Bugsa',
                'Judy Hopps',
                'Shini Waifu',
            ] 
        },
}

class FuckMarryKill(MiniGame):
    def __init__(self, players: dict[str, Player]):
        self.players: dict[str, Player] = players
        self.persons: list[str] = random.sample(random.choice(list(random.choice(list(PERSONS.values())).values())), k=3)
        self.votes: dict = {}

        self.finished = False

    def get_state(self, player_id: str):
        return {
            "persons": self.persons,
            "finished": self.finished,
            "results": self.results if self.finished else {}
        }

    def set_info(self, player_id: str, info: dict[str, Any]):
        if not self.finished:
            if 'vote' in info and player_id not in self.votes:
                self.votes[player_id] = info['vote']
                print(self.votes, self.players)

                if len(self.votes) == len(self.players):
                    print('finished##############################')
                    self.calculate_scores()
                    self.finished = True

    def calculate_scores(self):
        self.results = {}
        for player_id, vote in self.votes.items():
            money = 0
            for category in ["kill", "marry", "fuck"]:
                choice = vote[category]
                matches = sum(
                    1
                    for other_id, other_vote in self.votes.items()
                    if other_id != player_id
                    and other_vote[category] == choice
                )
                money += matches * 10
            self.players[player_id].money += money
            self.results[player_id] = {
                "money": money,
                "vote": vote
            }


