from typing import List
from enum import Enum
from random import randint, shuffle

from faker import Faker


FAKE = Faker()


class CardType(Enum):
    AMBASSADOR = 'ambassador'
    ASSASSIN = 'assassin'
    CAPTAIN = 'captain'
    CONTESSA = 'contessa'
    DUKE = 'duke'
    
    def __repr__(self):
        return self.name


class Face(Enum):
    UP = 'up'
    DOWN = 'down'

    def __repr__(self):
        return self.name


class Card:
    def __init__(self, card_type):
        self.card = card_type
        self.face = Face.DOWN

    def __repr__(self):
        return f'{self.card.name} {self.face.name}'


class Deck:
    def __init__(self):
        self.cards = []
        for card in range(3):
            self.cards += [
                Card(CardType.AMBASSADOR),
                Card(CardType.ASSASSIN),
                Card(CardType.CAPTAIN),
                Card(CardType.CONTESSA),
                Card(CardType.DUKE),
            ]
        shuffle(self.cards)


class Player:
    def __init__(self, game, cards: List[Card], position: int, is_bot: bool=True, name=None):
        self.game = game
        if name is None:
            while name is None or name.lower() in [
                player.name.lower() for player in self.game.players
            ] or name.lower() == self.game.non_bot_name.lower():
                name = FAKE.unique.first_name()
            self.name = name
        else:
            self.name = name
        self.is_bot = is_bot
        self.coins = 2
        self.cards = cards
        self.position = position
        self.is_out = False

    def is_turn(self):
        return self.position == self.game.player_turn

    def __repr__(self):
        return self.name


class Game:
    def __init__(self, name='nobody', player_count=6, won=False):
        
        assert 2 <= player_count <=6 
        self.player_count = player_count
        self.player_turn = 0
        self.player_turn_complete = False
        self.non_bot_name = name
        self.non_bot_position = 0 if won else randint(0, player_count-1)
        if player_count == 2:
            self.treasury = 47
        else:
            self.treasury = 50 - (player_count * 2)
        self.court_deck = Deck()
        self.players = []
        
        for player in range(player_count):
            if player == self.non_bot_position:
                self.players.append(
                    Player(
                        game=self,
                        cards=[
                            self.court_deck.cards.pop(),
                            self.court_deck.cards.pop(),
                        ],
                        position=player,
                        is_bot=False,
                        name=name,
                    )
                )
            else:
                self.players.append(
                    Player(
                        game=self,
                        cards=[
                            self.court_deck.cards.pop(),
                            self.court_deck.cards.pop(),
                        ],
                        position=player,
                        is_bot=True,
                    )
                )

        if player_count == 2:
            self.players[0].coins = 1

        self.game_over = False

    def __repr__(self):
        return str(id(self))
