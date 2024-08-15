import numpy as np
from collections import OrderedDict

from rlcard.envs import Env

from rlcard.games.schnapsen import Game

from rlcard.games.schnapsen.utils import utils

class SchnapsenEnv(Env):
     
    def __init__(self, config):
        self.name = 'schnapsen'
        self.game = Game()
        super().__init__(config=config)
        self.state_shape = [[1, 7, 21] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]
        self._utils = utils


    def _extract_state(self, state):
        ''' Extract useful information from state for RL. Must be implemented in the child class.

        Args:
            state (dict): The raw state

        Returns:
            (numpy.array): The extracted state
        '''
        extracted_state = {}

        current_player = self.game.get_current_player()
        opponent = self.game.round.players[(current_player.player_id + 1) % 2]

        stock_pile = self.game.round.dealer.stock_pile
        is_closed = state["is_closed"]

        encoded_hand = utils.encode_cards(current_player.hand,is_closed)
        won_cards = utils.encode_cards(current_player.won_tricks,is_closed)
        known_cards = utils.encode_cards(current_player.known_cards,is_closed)

        oponnent_won_cards = utils.encode_cards(opponent.won_tricks,is_closed)
        oponnent_known_cards = utils.encode_cards(opponent.known_cards,is_closed)

        unknown_cards = stock_pile + [card for card in opponent.hand]
        for card in unknown_cards:
            if card in known_cards:
                unknown_cards.remove(card)

        encoded_unknown_cards = utils.encode_cards(unknown_cards,is_closed)

        encoded_currentTrick = utils.encode_cards(state["current_trick"],is_closed)

        rep = [encoded_hand, won_cards, oponnent_won_cards, known_cards, oponnent_known_cards, encoded_unknown_cards, encoded_currentTrick]
        obs = np.array(rep)
        extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions(), 'raw_legal_actions': list(self._get_legal_actions().keys())}
        extracted_state['raw_obs'] = obs
        
        return extracted_state
    
    def get_payoffs(self):
        ''' Get the payoffs of players. Must be implemented in the child class.

        Returns:
            payoffs (list): a list of payoffs for each player
        '''
        print(self.game.round.move_sheet)
        print("==========================")
        print(self.game.get_payoffs())
        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id: int):
        ''' Decode Action id to the action in the game.

        Args:
            action_id (int): The id of the action

        Returns:
            (string): The action that will be passed to the game engine.

        Note: Must be implemented in the child class.
        '''
        x = self.game.my_decode_action(action_id)
        return x

    def _get_legal_actions(self):
        ''' Get all legal actions for current state.

        Returns:
            (list): A list of legal actions' id.

        Note: Must be implemented in the child class.
        '''
        current_player_id = self.game.round.get_current_player_id()
        legal_actions = self.game.round.get_legal_actions(current_player_id)
        legal_actions_ids = {action_event.action_id: None for action_event in legal_actions}
        return OrderedDict(legal_actions_ids)
