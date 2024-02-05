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
    self.settings = Settings()
    self.actions = None  # type: List[ActionEvent] or None # must reset in init_game
    self.round = None  # round: GinRummyRound or None, must reset in init_game
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