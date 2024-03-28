from .player import SchnapsenPlayer
from .utils import utils as utils
from rlcard.games.schnapsen.schnapsencard import SchnapsenCard

class SchnapsenDealer:
    ''' Initialize a SchnapsenDealer class
    '''
    def __init__(self, np_random):
        ''' Empty discard_pile, set shuffled_deck, set stock_pile
        '''
        self.np_random = np_random
        self.shuffled_deck = SchnapsenCard.get_deck()  # keep a copy of the shuffled cards at start of new hand
        self.np_random.shuffle(self.shuffled_deck)
        self.stock_pile = self.shuffled_deck.copy()  
        self.__trump_suit = self.stock_pile[0].suit

    def deal_cards(self, player: SchnapsenPlayer):
        ''' Deal some cards from stock_pile to one player

        Args:
            player (SchnapsenPlayer): The SchnapsenPlayer object
            num (int): The number of cards to be dealt
        '''
        for _ in range(5):
            player.hand.append(self.stock_pile.pop())

    def trumpExchange(self, SchnapsenCard):
        if(len(self.stock_pile) >= 2):
            old = self.stock_pile.pop(0)
            self.stock_pile.insert(0,SchnapsenCard)
            return old
        return None
    
    def trumpCard(self):
        """Returns the current trump card, i.e., the bottommost card.
        Or None in case this Talon is empty
        """
        if len(self.stock_pile) > 0:
            return self.stock_pile[0]
        return None
    
    def trumpSuit(self):
        """Return the suit of the trump card, i.e., the bottommost card.
        This still works, even when the Talon has become empty.
        """
        return self.__trump_suit
    
    def trumpCard(self):
        """Return the suit of the trump card, i.e., the bottommost card.
        This still works, even when the Talon has become empty.
        """
        return self.stock_pile[0]
    

