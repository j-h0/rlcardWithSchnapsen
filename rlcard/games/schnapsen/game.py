import numpy as np
from copy import deepcopy

from .player import SchnapsenPlayer
from .round import SchnapsenRound
from .judger import SchnapsenJudger
from .utils.schnapsen_action_event import *
#from .utils.settings import Settings, DealerForRound

from .utils.schnapsen_action_event import *

class SchnapsenGame:
    def __init__(self, allow_step_back=True):
        '''Initialize the class GinRummyGame
        '''
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.judge = SchnapsenJudger()
        self.actions = None  # type: List[ActionEvent] or None # must reset in init_game
        self.round = None  # round: SchnapsenRound or None, must reset in init_game
        self.num_players = 2
        # Save the hisory for stepping back to the last state.
        self.history = []

    def init_game(self):
        ''' Initialize all characters in the game and start round 1
        '''
        start_leader_id = self.np_random.choice([0, 1])
        self.actions = []
        self.round = SchnapsenRound(start_leader_id=start_leader_id, np_random=self.np_random)
        for i in range(2):
            player = self.round.players[i]
            self.round.dealer.deal_cards(player=player)
        current_player_id = self.round.leader
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
        
        if isinstance(action, TrumpExchangePlayerAction):
            self.round.trumpExchange(action)
        elif isinstance(action, SixsixAction):
            self.round.claimSixSix(action)
        elif isinstance(action, MarriagePlayerAction):
            self.round.marriage(action)
        elif isinstance(action, CloseTalonAction):
            self.round.closeTalon(action)
        elif isinstance(action, PlayCardAction):
            self.round.play_card(action)
        else:
            raise Exception('Unknown step action={}'.format(action))
        self.actions.append(action)
        if (len(self.round.current_trick)>0):
            next_player_id = self.round.follower
        else:
            next_player_id = self.round.leader
        next_state = self.get_state(player_id=next_player_id)

        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))
        
        return next_state, next_player_id


    def step_back(self):
        ''' Takes one step backward and restore to the last state
        '''
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def get_num_players(self):
        ''' Return the number of players in the game
        '''
        return 2

    def get_state(self, player_id: int):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        state = self.round.get_state(player_id)
        
        current_player_id = self.round.get_current_player_id()

        state['current_player'] = current_player_id
        #state['legal_actions'] = self.round.get_legal_actions(current_player_id)
        return state

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        emptydeck = False
        if not self.round.dealer.stock_pile:
            emptydeck = True
        x,y = self.judge.judge_game(self.round.players[self.round.leader],self.round.players[self.round.follower],emptydeck)
        
        return x,y

    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 61 actions
        '''
        return 27

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.round.get_current_player_id()
    
    def get_current_player(self) -> SchnapsenPlayer or None:
        return self.round.get_current_player()

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        return self.round.is_over
    
    def my_decode_action(self, action_id: int):
        return ActionEvent.decode_action(action_id=action_id)