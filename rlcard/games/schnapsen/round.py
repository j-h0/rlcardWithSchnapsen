from rlcard.games.schnapsen.dealer import SchnapsenDealer
from rlcard.games.schnapsen.judger import SchnapsenJudger
from rlcard.games.schnapsen.player import SchnapsenPlayer
from rlcard.games.schnapsen.utils.utils import Moves
from rlcard.games.schnapsen.utils.utils import filter_hand

from .utils.schnapsen_action_event import *

class SchnapsenRound: 

    def __init__(self, start_leader_id: int, np_random):
        ''' Initialize the round class

        The round class maintains the following instances:


        Args:

        '''
        self.np_random = np_random

        self.dealer = SchnapsenDealer(np_random = np_random)

        self.trump_suit = self.dealer.trumpSuit()

        self.target = None

        self.is_closed = False

        self.leader = start_leader_id

        self.follower = (start_leader_id + 1) % 2

        self.is_over = False

        shuffled_deck = self.dealer.shuffled_deck

        self.players = [SchnapsenPlayer(player_id=0, np_random=self.np_random),
                         SchnapsenPlayer(player_id=1, np_random=self.np_random)]

        self.current_trick = []

        self.all_tricks = []

        self.move_sheet = []  # type: List[GinRummyMove]

        self.winner = None


    def get_current_player(self) -> SchnapsenPlayer or None:
        current_player_id = self.get_current_player_id()
        return None if current_player_id is None else self.players[current_player_id]
    
    def get_current_player_id(self):
        if(len(self.current_trick) > 0):
            return self.follower
        else:
            return self.leader

    def draw_card(self,player):
        if(self.is_closed):
            return
        if(len(self.dealer.stock_pile) <= 0):
            self.is_closed = True
            return
        card = self.dealer.stock_pile.pop()
        self.players[player].hand.append(card)

    def play_card(self, action: PlayCardAction):
                # when current_player takes PlayCardAction step, the move is recorded and executed
        current_player = self.get_current_player()
        card = action.card
        current_player.hand.remove(card)
        self.current_trick.append(card)



        if(len(self.current_trick) == 2):

            self.leader, self.follower, winner = SchnapsenJudger.judge_trick(self.leader,self.follower,self.current_trick,self.dealer.trumpSuit())
            self.players[self.leader].won_tricks += self.current_trick
            self.current_player_id = self.leader

            self.current_trick.clear()
            self.draw_card(self.leader)
            self.draw_card(self.follower)
  

        return None

    def marriage(self, action: MarriagePlayerAction):
        current_player = self.players[self.current_player_id]
        suit = action.suit
        if(suit == self.trump_suit):
            current_player.points += 40
        else:
            current_player.points += 20    
        queen = filter_hand(current_player.hand,2,suit)[0]
        self.play_card(PlayCardAction(queen))


    def trumpExchange(self, action: TrumpExchangePlayerAction):
        current_player = self.players[self.current_player_id]
        trumpJack = SchnapsenCard.get_trump_jack(self.trump_suit)
        current_player.hand.remove(trumpJack)
        card = self.dealer.trumpExchange(trumpJack)
        current_player.hand.append(card)

    def closeTalon(self, action: CloseTalonAction):
        self.is_closed = True

    def claimSixSix(self, action: SixsixAction):
        self.is_over = True

    def get_legal_actions(self, playerId):
        legal_actions = []
        playable_cards = []
        hand = self.players[playerId].hand

        if(playerId == self.leader):
            legal_actions = Moves.get_legal_leader_moves(self.get_state(playerId), hand)
        else:
            legal_actions = Moves.get_legal_follower_moves(self.get_state(playerId), hand)

        return legal_actions
    


    def get_state(self, player_id: int):
        ''' Get player's state
        Return:
            state (dict): The information of the state
        '''
        state = {}
        #(valid_act, player, cards) = self.judger.judge_pong_gong(self.dealer, players, self.last_player)

        state['is_leader'] = self.leader == player_id
        state['current_hand'] = self.players[player_id].hand
        state['current_trick'] = self.current_trick 
        state['all_tricks'] = self.all_tricks
        state['is_closed'] = self.is_closed
        state['trump_suit'] = self.dealer.trumpSuit()
        if not self.dealer.stock_pile:
            if not self.players[self.follower].hand:
                self.is_over = True
        return state






