from rlcard.games.base import Card
from typing import List, Iterable


class SchnapsenCard(Card):
    suits = ['H', 'S', 'E', 'L']
    ranks = [10, 2, 3, 4, 11]


    @staticmethod
    def card(card_id: int):
        return _deck[card_id]

    @staticmethod
    def get_deck() -> [Card]:
        return _deck.copy()

    def __init__(self, suit: str, rank: str):
        super().__init__(suit=suit, rank=rank)
        self.suit_index = SchnapsenCard.suits.index(self.suit)
        rank_index = SchnapsenCard.ranks.index(self.rank)
        self.card_id = 5 * self.suit_index + rank_index

    def __str__(self):
        return f'{self.rank}{self.suit}'

    def __repr__(self):
        return f'{self.rank}{self.suit}'
    
    def get_card_id(self):
        return self.card_id
    
    def get_suit_idx(self):
        return self.suit_index
    
    @staticmethod
    def get_trump_jack(trump_suit):
        for card in _deck:
            if card.rank == 2 and card.suit == trump_suit:
                return card


# deck is always in order from 2C, ... KC, AC, 2D, ... KD, AD, 2H, ... KH, AH, 2S, ... KS, AS
_deck = [SchnapsenCard(suit=suit, rank=rank) for suit in SchnapsenCard.suits for rank in SchnapsenCard.ranks]  # want this to be read-only
