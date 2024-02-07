from .player import SchnapsenPlayer
from .utils import utils as utils


class SchnapsenDealer:
    ''' Initialize a SchnapsenDealer class
    '''
    def __init__(self, np_random):
        ''' Empty discard_pile, set shuffled_deck, set stock_pile
        '''
        self.np_random = np_random
        self.discard_pile = []  # type: List[Card]
        self.shuffled_deck = utils.get_deck()  # keep a copy of the shuffled cards at start of new hand
        self.np_random.shuffle(self.shuffled_deck)
        self.stock_pile = self.shuffled_deck.copy()  # type: List[Card]
        self.trump_card = None

    def deal_cards(self, player: SchnapsenPlayer, num: int):
        ''' Deal some cards from stock_pile to one player

        Args:
            player (SchnapsenPlayer): The SchnapsenPlayer object
            num (int): The number of cards to be dealt
        '''
        for _ in range(num):
            player.hand.append(self.stock_pile.pop())
        player.did_populate_hand()

    def trumpExchange(SchnapsenCard):
        old = self.trump_card
        self.trump_card = SchnapsenCard
        return old
