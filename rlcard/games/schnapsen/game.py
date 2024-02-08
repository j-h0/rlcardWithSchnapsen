import numpy as np

from .player import GinRummyPlayer
from .round import GinRummyRound
from .judge import GinRummyJudge
from .utils.settings import Settings, DealerForRound

from .utils.action_event import *

class SchnapsenGame:
    def __init__(self, allow_step_back=False):
        '''Initialize the class GinRummyGame
        '''
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.judge = GinRummyJudge(game=self)
        self.actions = None  # type: List[ActionEvent] or None # must reset in init_game
        self.round = None  # round: SchnapsenRound or None, must reset in init_game
        self.num_players = 2

    def init_game(self):
        ''' Initialize all characters in the game and start round 1
        '''
        dealer_id = self.np_random.choice([0, 1])
        if self.settings.dealer_for_round == DealerForRound.North:
            dealer_id = 0
        elif self.settings.dealer_for_round == DealerForRound.South:
            dealer_id = 1
        self.actions = []
        self.round = GinRummyRound(dealer_id=dealer_id, np_random=self.np_random)
        for i in range(2):
            num = 11 if i == 0 else 10
            player = self.round.players[(dealer_id + 1 + i) % 2]
            self.round.dealer.deal_cards(player=player, num=num)
        current_player_id = self.round.current_player_id
        state = self.get_state(player_id=current_player_id)
        return state, current_player_id

    def step(self, action):
        ''' Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''

        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))

        self.round.proceed_round(self.players, action)
        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step_back(self):
        ''' Takes one step backward and restore to the last state
        '''
        raise NotImplementedError

    def get_num_players(self):
        ''' Return the number of players in the game
        '''
        return 2

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        state = self.round.get_state(self.players, player_id)
        state['num_players'] = self.get_num_players()
        state['current_player'] = self.round.current_player
        return state

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        winner = self.round.winner
        if winner is not None and len(winner) == 1:
            self.payoffs[winner[0]] = 1
            self.payoffs[1 - winner[0]] = -1
        return self.payoffs

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player, self.round.roundTrump, self.round.)


    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 61 actions
        '''
        return 61

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.round.current_player

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        return self.round.is_over