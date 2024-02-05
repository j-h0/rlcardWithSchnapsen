from rlcard.games.base import Card


class SchnapsenCard(Card):
    suits = ['H', 'S', 'E', 'L']
    ranks = ['T', 'J', 'Q', 'K', 'A']


    @staticmethod
    def card(card_id: int):
        return _deck[card_id]

    @staticmethod
    def get_deck() -> [Card]:
        return _deck.copy()

    def __init__(self, suit: str, rank: str):
        super().__init__(suit=suit, rank=rank)
        suit_index = SchnapsenCard.suits.index(self.suit)
        rank_index = SchnapsenCard.ranks.index(self.rank)
        self.card_id = 13 * suit_index + rank_index

    def __str__(self):
        return f'{self.rank}{self.suit}'

    def __repr__(self):
        return f'{self.rank}{self.suit}'


# deck is always in order from 2C, ... KC, AC, 2D, ... KD, AD, 2H, ... KH, AH, 2S, ... KS, AS
_deck = [SchnapsenCard(suit=suit, rank=rank) for suit in SchnapsenCard.suits for rank in SchnapsenCard.ranks]  # want this to be read-only