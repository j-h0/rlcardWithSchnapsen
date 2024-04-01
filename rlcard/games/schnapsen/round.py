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

        self.is_closed = False

        self.leader = start_leader_id

        self.follower = (start_leader_id + 1) % 2

        self.is_over = False

        self.players = [SchnapsenPlayer(player_id=0, np_random=self.np_random),
                         SchnapsenPlayer(player_id=1, np_random=self.np_random)]

        self.current_trick = []

        self.move_sheet = [self.trump_suit]  # type: List[GinRummyMove]

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
        card = self.dealer.drawCard()
        if card is None:
            print("wtf: ",self.is_closed)
        self.players[player].hand.append(card)

    def play_card(self, action: PlayCardAction):
                # when current_player takes PlayCardAction step, the move is recorded and executed
        current_player = self.get_current_player()
        card = action.card
        self.move_sheet.append([current_player.get_player_id(),"Playcard", card])
        current_player.hand.remove(card)
        self.current_trick.append(card)



        if(len(self.current_trick) == 2):

            self.leader, self.follower, winner = SchnapsenJudger.judge_trick(self.leader,self.follower,self.current_trick,self.dealer.trumpSuit())
            self.players[self.leader].won_tricks += self.current_trick
            self.players[self.leader].points += (self.current_trick[0].rank + self.current_trick[1].rank)
            self.players[self.follower].known_cards.append(self.current_trick[0])
            self.players[self.follower].known_cards.append(self.current_trick[1])
            self.current_player_id = self.leader

            self.current_trick.clear()
            self.draw_card(self.leader)
            self.draw_card(self.follower)
  

    def marriage(self, action: MarriagePlayerAction):
        current_player = self.get_current_player()
        suit = SchnapsenCard.suits[action.suit]
        self.move_sheet.append([current_player.get_player_id(),"Marriage", suit])
        if(suit == self.trump_suit):
            current_player.points += 40
        else:
            current_player.points += 20 
        queen = filter_hand(current_player.hand,3,suit)[0]
        king = filter_hand(current_player.hand,4,suit)[0]

        self.players[self.follower].known_cards.append(king)

        self.play_card(PlayCardAction(queen))


    def trumpExchange(self, action: TrumpExchangePlayerAction):
        if self.is_closed or not self.dealer.stock_pile:
            print("WHHHYYYYY")
            return
        current_player = self.get_current_player()
        self.move_sheet.append([current_player.get_player_id(),"trumpexchange"])
        trumpJack = SchnapsenCard.get_trump_jack(self.trump_suit)
        if trumpJack is None:
            print("WTF")
        current_player.hand.remove(trumpJack)
        card = self.dealer.trumpExchange(trumpJack)
        if card is None:
            print("wtf: ",self.is_closed)
        current_player.hand.append(card)
        self.players[self.follower].known_cards.append(card)

    def closeTalon(self, action: CloseTalonAction):
        self.is_closed = True

    def claimSixSix(self, action: SixsixAction):
        self.is_over = True

    def get_legal_actions(self, playerId):
        legal_actions = []
        hand = self.players[playerId].hand

        if(playerId == self.leader):
            legal_actions = Moves.get_legal_leader_moves(self.get_state(playerId), self.get_current_player())
        else:
            legal_actions = Moves.get_legal_follower_moves(self.get_state(playerId), hand)

        if not legal_actions:
            self.is_over = True

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
        state['is_closed'] = (self.is_closed or len(self.dealer.stock_pile) == 0)
        state['trump_suit'] = self.dealer.trumpSuit()
        if not self.dealer.stock_pile:
            if not self.players[self.follower].hand:
                self.is_over = True
        return state






