import numpy as np
from collections import OrderedDict

from rlcard.envs import Env

class SchnapsenEnv(Env):
     
    def __init__(self, config):


        self.name = 'schnapsen'
        self.game = Game()
        super().__init__(config=config)
        self.state_shape = [[5, 52] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):
        ''' Extract useful information from state for RL. Must be implemented in the child class.

        Args:
            state (dict): The raw state

        Returns:
            (numpy.array): The extracted state
        '''

        if self.game.is_over():
            obs = np.array([self])
        else:
            stiche_playerOne = self.game.round.dealer.stiche_playerOne
            stiche_playerTwo = self.game.round.dealer.stiche_playerTwo
            unknown_cards = stock_pile + [card for card in opponent.hand if card not in known_cards]
            game_state = self.game.round.dealer.game_state
        raise NotImplementedError

    def _decode_action(self, action_id):
        ''' Decode Action id to the action in the game.

        Args:
            action_id (int): The id of the action

        Returns:
            (string): The action that will be passed to the game engine.

        Note: Must be implemented in the child class.
        '''
        raise NotImplementedError

    def _get_legal_actions(self):
        ''' Get all legal actions for current state.

        Returns:
            (list): A list of legal actions' id.

        Note: Must be implemented in the child class.
        '''
        raise NotImplementedError
