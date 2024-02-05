from typing import List

from rlcard.games.base import Card

from .utils import utils

from .utils import melding


class SchnapsenPlayer:

    def __init__(self, player_id: int, np_random):
        ''' Initialize a GinRummy player class

        Args:
            player_id (int): id for the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []  # type: List[Card]
        self.known_cards = []  # type: List[Card]  # opponent knows cards picked up by player and not yet discarded
        # memoization for speed

    def get_state(self, public_card, all_chips, legal_actions):
        ''' Encode the state for the player

        Args:
            public_card (object): The public card that seen by all the players
            all_chips (int): The chips that all players have put in

        Returns:
            (dict): The state of the player
        '''
        state = {}
        state['hand'] = self.hand.get_index()
        state['public_card'] = public_card.get_index() if public_card else None
        state['all_chips'] = all_chips
        state['my_chips'] = self.in_chips
        state['legal_actions'] = legal_actions
        return state

    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id
