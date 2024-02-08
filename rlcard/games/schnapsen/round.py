from rlcard.games.schnapsen.schnapsencard import SchnapsenCard
from rlcard.games.schnapsen.dealer import SchnapsenDealer
from rlcard.games.schnapsen.judger import SchnapsenJudger
from .player import SchnapsenPlayer
from rlcard.games.schnapsen.utils.utils import Moves



class SchnapsenRound:

    def __init__(self, start_leader_id: int, np_random):
        ''' Initialize the round class

        The round class maintains the following instances:


        Args:

        '''
        self.np_random = np_random

        self.dealer = SchnapsenDealer

        self.target = None

        self.is_closed = False

        self.leader = start_leader_id

        self.follower = (start_leader_id + 1) % 2

        self.is_over = False

        shuffled_deck = self.dealer.shuffled_deck

        self.current_trick = []

        self.tricks = []

        self.move_sheet = []  # type: List[GinRummyMove]

        self.is_over = False

        self.winner = None

    def get_current_player(self) -> SchnapsenPlayer or None:
        current_player_id = self.current_player_id
        return None if current_player_id is None else self.players[current_player_id]

    def draw_card(self, action: DrawCardAction):
        if(self.is_closed):
            return
        if(len(self.dealer.stock_pile) <= 0):
            is_closed = True
            return
        
        current_player = self.players[self.current_player_id]
        card = self.dealer.stock_pile.pop()
        current_player.hand.append(card=card)

    def marriage(self, action: MarriageAction):
        self.np_random = np_random

    def trumpExchange(self, action: TrumpExchangeAction):
        current_player = self.players[self.current_player_id]
        card = current_player.hand.remove(action.card)
        card = self.dealer.trumpExchange(card)
        current_player.hand.append(card)

    def closing(self, action: Cloremove_card_from_handsingAction):
        self.is_closed = True
        return None

    def claimSixSix(self, action: SixSixAction):
        self.is_over = True
        return None
    
    def get_legal_actions(self, players, player_id):
        legal_actions = []
        playable_cards = []
        hand = players[player_id].hand

        if(player_id == self.leader):
            legal_actions = Moves.get_legal_leader_moves()
        elif(not trick is None):
            legal_actions = Moves.get_legal_leader_moves()
        else:
            legal_actions.append(passAction)

        return legal_actions
    
    def play_card(self, action: PlayCardAction):
                # when current_player takes PlayCardAction step, the move is recorded and executed
        current_player = self.players[self.current_player_id]
        self.move_sheet.append(PlayCardMove(current_player, action))
        card = action.card
        self.current_trick.append(self.current_player.hand.pop(action.card))


        if(len(self.current_trick) == 2):
            leader, follower, winner = SchnapsenJudger.judge_trick()
            self.tricks[leader].append(self.current_trick)
            self.current_trick.clear()
  

        return None

    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of MahjongPlayer
            player_id (int): The id of the player
        Return:
            state (dict): The information of the state
        '''
        state = {}
        #(valid_act, player, cards) = self.judger.judge_pong_gong(self.dealer, players, self.last_player)
        if self.valid_act: # PONG/GONG/CHOW
            state['valid_act'] = [self.valid_act, 'stand']
            state['table'] = self.dealer.table
            state['player'] = self.current_player
            state['current_hand'] = players[self.current_player].hand
            state['players_pile'] = {p.player_id: p.pile for p in players}
            state['action_cards'] = self.last_cards # For doing action (pong, chow, gong)
        else: # Regular Play
            state['valid_act'] = ['play']
            state['table'] = self.dealer.table
            state['player'] = self.current_player
            state['current_hand'] = players[player_id].hand
            state['players_pile'] = {p.player_id: p.pile for p in players}
            state['action_cards'] = players[player_id].hand # For doing action (pong, chow, gong)
        return state






